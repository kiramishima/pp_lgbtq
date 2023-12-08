import psycopg

with psycopg.connect(f'host=192.168.100.47 dbname=alerta_272 user=postgres password=123456') as connection:
    with connection.cursor() as cur:
        query = 'SELECT COUNT(*) c FROM tipos_reportantes WHERE tipo_reportante = %s'
        # cur.prepare(query)
        newItems = []
        for item in ['Testiga', 'Elite', 'Personal']:
            result = cur.execute(query, (item,)).fetchone()
            print('Result', result)
            if not result[0]:
                newItems.append(item)

        print('New Items', newItems)