import os
import pandas as pd
import numpy as np
import datetime as dt
from airflow.models import Variable

DB_CONN = Variable.get('SQL_CONNECTION', default_var='host=192.168.100.47 dbname=alerta_272 user=postgres password=123456')

def get_df(ti, **kwargs):
    ''' Leé multiples datos y los mete en un solo Dataframe '''
    try:
        paths = ti.xcom_pull(task_ids='Obtener_Listado_Archivos_CSV_De_Hadoop', key='files_list')
        # print('files', paths)

        if len(paths)==0:
            raise ValueError("No hay archivos en el directorio de Hadoop")

        # Leemos el CSV con los datos
        dfs = []
        for file in paths:
            df_temp = pd.read_csv(file, **kwargs)
            dfs.append(df_temp)

        df = pd.concat(dfcols, ignore_index=True)
        print('df', df.shape)
        return df
    except Exception as err:
        print(err)

def load_data_to_pandas(ti):
    """ Carga toda la información al Dataframe """

    # Cargamos la información de los reportes
    df_reportes = get_df(ti, encoding='latin1')
    print('df_reporte', df_reportes.shape)
    print('df_reporte_columns', df_reportes.columns)
    # Procesamos las columnas que queremos agregar si hay nuevos datos en las tablas relacionales
    data = dict(
        reportante=process_column(df_reportes[df_reportes['reportante'].notna()]['reportante']),
        ttestigos=process_column(df_reportes[df_reportes['tipo_de_testiga'].notna()]['tipo_de_testiga']),
        tvictimas=process_column(df_reportes[df_reportes['tipo_de_victima'].notna()]['tipo_de_victima']),
        redades=process_column(df_reportes[df_reportes['edad_victima'].notna()]['edad_victima']),
        idxgenero=process_column(df_reportes[df_reportes['identidad_genero'].notna()]['identidad_genero']),
        osexual=process_column(df_reportes[df_reportes['orientacion_sexual'].notna()]['orientacion_sexual']),
        expgenero=process_column(df_reportes[df_reportes['expresion_genero'].notna()]['expresion_genero']),
        tagresora=process_column(df_reportes[df_reportes['tipo_de_agresora'].notna()]['tipo_de_agresora']),
        tagresion=process_column(df_reportes[df_reportes['tipo_de_agresion'].notna()]['tipo_de_agresion']),
        stagresion=process_relational_columns('tipo_de_agresion', 'subtipo_de_agresion', df_reportes),
        entidades=process_column(df_reportes[df_reportes['entidad'].notna()]['entidad']),
        entidadciudades=process_relational_columns('entidad', 'ciudad', df_reportes),
        tlugar=process_column(df_reportes[df_reportes['tipo_de_lugar'].notna()]['tipo_de_lugar']),
        stlugar=process_relational_columns('tipo_de_lugar', 'subtipo_de_lugar', df_reportes),
        lreporte_previo_quien=process_column(df_reportes[df_reportes['reporte_previo_quien'].notna()]['reporte_previo_quien']),
        leciviles=process_column(df_reportes[df_reportes['estado_civil'].notna()]['estado_civil']),
        lnacionalidades=process_column(df_reportes[df_reportes['nacionalidad'].notna()]['nacionalidad']),
        lescolaridades=process_column(df_reportes[df_reportes['escolaridad'].notna()]['escolaridad']),
        locupaciones=process_column(df_reportes[df_reportes['ocupacion'].notna()]['ocupacion']),
        lingresos=process_column(df_reportes[df_reportes['ingreso'].notna()]['ingreso']),
        lss=process_column(df_reportes[df_reportes['seguridad_social'].notna()]['seguridad_social']),
        lidentidades=process_column(df_reportes[df_reportes['identidades'].notna()]['identidades'])
    )

    # Se envia la data hacia la Pipeline: Procesar_Registros
    ti.xcom_push(key='data', value=data)
    # Se envia la data hacia la Pipeline: Procesar_Registros
    ti.xcom_push(key='records', value=df_reportes.to_dict("records"))


def process_column(col: pd.Series):
    """ Retorna el listado de valores unicos de la columna """
    return col.unique().tolist().sort()


def process_relational_columns(parent: str, child: str, df: pd.DataFrame):
    """ Retorna el listado de valores unicos de la forma padre - hijo """
    g = df[df[parent].notna() & df[child].notna()].groupby(parent, sort=True)[child].agg(['unique'])
    data = []
    for _, item_cat in enumerate(g.index):
        items = [x for x in g.loc[item_cat].values.tolist()]
        # print(items)
        for item in items:
            for x in item:
                data.append((item_cat, x))
    return data

def filter_new_data_cols(ti):
    '''Selecciona los nuevos datos para las tablas'''
    import psycopg

    data = ti.xcom_pull(task_ids='Procesar_Datos', key='data')
    print('data', data)
    print('data type', type(data))
    newItems = {}
    with psycopg.connect(DB_CONN) as connection:
        with connection.cursor() as cur:
            for key, items in data.items():
                if not items is None:
                    match key:
                        case 'reportante':
                            # query
                            if newItems.get(key) is None:
                                newItems[key] = []

                            query = 'SELECT COUNT(*) c FROM tipos_reportantes WHERE tipo_reportante = %s'
                            for item in items:
                                result = cur.execute(query, (item,)).fetchone()
                                if not result[0]:
                                    newItems[key].append(item)

                            print('Key "{}" has new {} items'.format(key, len(newItems[key])))

    ti.xcom_push(key='new_data', value=newItems)



def transform_data_rows(ti):
    '''Selecciona los nuevos registros'''
    data = ti.xcom_pull(task_ids='Procesar_Datos', key='records')
    print('data', data)
    print('data type', type(data))
    newItems = []
    with psycopg.connect(DB_CONN) as connection:
        with connection.cursor() as cur:
            for item in data.get('records'):
                query = 'SELECT COUNT(*) c FROM processed_reports WHERE ref_report_id = %s'
                result = cur.execute(query, (item['id'],)).fetchone()
                if not result[0]:
                    newItems.append(item)

    ti.xcom_push(key='new_records', value=newItems)