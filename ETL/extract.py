import os
import re
from airflow.models import Variable
from hdfs import InsecureClient

# Datos de conexión
HDFS_HOSTNAME = Variable.get('HDFS_HOST', default_var='192.168.100.13')
HDFSCLI_PORT = Variable.get('HDFS_PORT', default_var=9870)
HDFSCLI_CONNECTION_STRING = f'http://{HDFS_HOSTNAME}:{HDFSCLI_PORT}'

def get_files_if_exists(ti):
    """"
    Retorna una lista de archivos si hay archivos en la carpeta de input de Hadoop
    """
    dir_path = os.getenv('INPUT_HDFS_DIR', "/INPUT_DIR")

    # En nuestro caso, al no usar Kerberos, creamos una conexión no segura, pero es ambiente empresarial si debemos usar conexines seguras y algun Vault para manejar estos accesos.
    hdfs_client = InsecureClient(HDFSCLI_CONNECTION_STRING)

    files = [
        (f"http://{HDFS_HOSTNAME}:{HDFSCLI_PORT}/webhdfs/v1{dir_path}/{file}?op=OPEN", file) # URL de nuestra instancia local de Hadoop
        for file in hdfs_client.list(dir_path)
    ]

    ti.xcom_push(key='files_list', value=files)
    return len(files)
