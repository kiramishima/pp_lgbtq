import os
from airflow.models import Variable

DB_CONN = Variable.get('SQL_CONNECTION', default_var='host=192.168.100.47 dbname=alerta_272 user=postgres password=123456')

def load_columns_data_to_pg(ti):
    """ Carga la información de items de nuevas columnas a PG """
    import psycopg

    data = ti.xcom_pull(task_ids='Procesar_Columnas', key='new_data')
    print('data', data)
    print('data type', type(data))
    with psycopg.connect(DB_CONN) as connection:
        with connection.cursor() as cur:
            for key, items in data.items():
                if items is not None:
                    match key:
                        case 'reportante':
                            query = 'INSERT INTO tipos_reportantes(tipo_reportante) VALUES(%s)'
                            for item in items:
                                result = cur.execute(query, (item,)).fetchone()

                            print('Key "{}" has added new {} items'.format(key, len(items)))

    print('Proceso de Carga de datos nuevos en columnas terminado')


def load_records_data_to_pg(ti):
    """ Carga la información de los registros ya normalizada a PG """
    import psycopg

    data = ti.xcom_pull(task_ids='Procesar_Registros', key='new_records')
    print('data', data)
    print('data type', type(data))
    if not data is None:
        with psycopg.connect(DB_CONN) as connection:
            with connection.cursor() as cur:
                for key, items in data.items():
                    if items is not None:
                        match key:
                            case 'reportante':
                                query = 'CALL sp_insert_report(%s)'
                                for item in items:
                                    result = cur.execute(query, (item,)).fetchone()

                                print('Key "{}" has added new {} items'.format(key, len(items)))

        print('Proceso de Carga de datos nuevos registros terminado')
    else:
        print('No hay registros nuevos')