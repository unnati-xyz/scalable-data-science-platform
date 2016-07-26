import traceback
import os
import pandas as pd

from poget.utils.db import DBConn
from poget.utils.logger import Logger

LOGGER = Logger().get()


class BayBikeShare:
    def read_data(self):
        try:
            # reading data into dataframe
            dir = os.getcwd()
            data_dir = os.path.join(dir, 'data')
            csv_file = 'trip_data.csv'
            file_path = os.path.join(data_dir, csv_file)
            LOGGER.info("reading csv from %s"%file_path)
            data_df = pd.read_csv(file_path)

            return data_df
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e

    def load_data(self):
        try:
            # getting db connection
            conn = DBConn().get_sa_engine()
            # reading to data
            data_df = self.read_data()
            LOGGER.info("Writing to db")
            data_df.to_sql('trips', conn, if_exists='replace', index=False)
            LOGGER.info("DB write success")

        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e


if __name__ == "__main__":

    bike_share = BayBikeShare()
    bike_share.load_data()
