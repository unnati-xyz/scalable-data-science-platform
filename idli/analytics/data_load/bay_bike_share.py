import psycopg2
import traceback
import os
from sqlalchemy import create_engine

from idli.utils.db import DBConn
from idli.utils.logger import Logger

LOGGER = Logger().get()

class BayBikeShare:

    def read_data(self):
        try:
            # reading data into dataframe
            dir = os.getcwd()
            data_dir = os.path.join(dir, 'data')
            csv_file = 'trip_data.csv'
            file_path = os.path.join(data_dir, csv_file)
            data_df = pd.read_csv(file_path)
            return data_df
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e

     def load_data(self, inp_data):
         try:
            #getting db connection
            connection_string = DBConn().get_jdbc_url()
            #writing to db
            data_df.to_sql('trips_data', connection_string, if_exists='append')
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e
