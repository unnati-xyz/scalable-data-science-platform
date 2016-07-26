import psycopg2
from sqlalchemy import create_engine
from idli.config import configuration as cfg

class DBConn:


    def get_connection(self):
        conn = psycopg2.connect(database=cfg['db_name'], user=cfg['user'], host=cfg['host'],
                                port=cfg['port'], password=cfg['password'])

        return conn

    def get_jdbc_url(self):

        conn_url = "jdbc:postgresql://%s:%s/%s?user=%s&password=%s"%(cfg['host'],cfg['port']
                                                                     ,cfg['db_name'],cfg['user'],cfg['password'])
        return conn_url

    def get_connection_string(self):
        connection_string = cfg['db'] + '://' + cfg['user'] + ':' + \
                            cfg['password'] + '@' + cfg['host'] + '/' + \
                            cfg['db_name']

        return connection_string

    def get_sa_engine(self):

        return create_engine(self.get_connection_string())

