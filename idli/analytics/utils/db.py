import psycopg2
from idli.config import configuration as cfg

class DBConn:


    def get_connection(self):
        conn = psycopg2.connect(database=cfg['name'], user=cfg['user'], host=cfg['host'],
                                port=cfg['port'], password=cfg['password'])

        return conn

    def get_jdbc_url(self):

        conn_url = "jdbc:postgresql://%s:%s/%s?user=%s&password=%s"%(cfg['host'],cfg['port']
                                                                     ,cfg['name'],cfg['user'],cfg['password'])
        return conn_url
