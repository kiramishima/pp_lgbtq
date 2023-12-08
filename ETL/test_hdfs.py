from hdfs import InsecureClient
import pandas as pd
import os

# Datos de conexión
HDFS_HOSTNAME = '192.168.100.13'
HDFSCLI_PORT = 9870
HDFSCLI_CONNECTION_STRING = f'http://{HDFS_HOSTNAME}:{HDFSCLI_PORT}'

def get_files_if_exists():
    """"
    Para verificar si hay archivos en la carpeta de input
    """
    dir_path = os.getenv('INPUT_HDFS_DIR', "/INPUT_DIR")

    # En nuestro caso, al no usar Kerberos, creamos una conexión no segura
    hdfs_client = InsecureClient(HDFSCLI_CONNECTION_STRING, user='kiramishima')

    lisf = hdfs_client.list(dir_path)
    print('L', lisf)
    for file in lisf:
        hdfs_client.download(hdfs_path=f"{dir_path}/{file}", 
                            local_path='./csv',
                            n_threads=2,
                            temp_dir=None)

    #return files

files = get_files_if_exists()
print(files)

