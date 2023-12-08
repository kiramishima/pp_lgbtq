from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime as dt, timedelta
from extract import get_files_if_exists
from transform import load_data_to_pandas, filter_new_data_cols, transform_data_rows
from load import load_columns_data_to_pg, load_records_data_to_pg

default_args = {
    'owner': 'lcdn_504',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="etl_lgbtq_v1",
    description="DAG para el proceso ETL",
    start_date=dt(2023, 11, 28, 2),
    # start_date=dt(2023, 12, 31, 2), # Lo iniciara el 1ero de Junio a las 2AM
    schedule_interval="@monthly" # Ejecute cada mes
) as dag:

    # Tasks 1 - Listar archivos del directorio de entrada.
    task1 = PythonOperator(
        task_id="Obtener_Listado_Archivos_CSV_De_Hadoop",
        python_callable= get_files_if_exists,
        show_return_value_in_logs=True
    )
    # Task 2 - Procesar datos para transformarlos
    task2 = PythonOperator(
        task_id="Procesar_Datos",
        python_callable=load_data_to_pandas,
        show_return_value_in_logs=True
    )
    # Task 3 - Procesando Columnas
    task3 = PythonOperator(
        task_id="Procesar_Columnas",
        python_callable=filter_new_data_cols,
        show_return_value_in_logs=True
    )
    
    # Task 4 - Procesando Registros
    task4 = PythonOperator(
        task_id="Procesar_Registros",
        python_callable=transform_data_rows,
        show_return_value_in_logs=True
    )

    task5 = PythonOperator(
        task_id="Cargar_Registros_Nuevos_Columnas",
        python_callable=load_columns_data_to_pg,
        show_return_value_in_logs=True
    )

    task6 = PythonOperator(
        task_id="Cargar_A_PostgreSQL",
        python_callable=load_records_data_to_pg,
        show_return_value_in_logs=True
    )

    task1 >> task2 >> task3 >> task4 >> task5 >> task6
