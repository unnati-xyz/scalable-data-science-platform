import traceback
import pandas as pd
from poget.utils.db import DBConn
import poget.utils.ml as mlUtils
from poget import LOGGER

from poget.analytics.ml.logistic_regression import LogisticRegression
import os


# ## Hypothesis 1
#
# ### Given a time slot and terminal code, predict if the terminal has high traffic
class TerminalTraffic:


    def __init__(self):
        self.name = 'terminal-traffic'
        self.main_directory = 'poget'
        self.models_directory = 'models'
        self.name = 'prob_call'

    def get_data(self):
        try:

            conn = DBConn().get_connection()
            query = '''SELECT * from trips '''
            LOGGER.info("Reading data from db : %s"%(query))
            df = pd.read_sql(query, con=conn)

            return df

        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e


    # ### Feature engineering
    #
    # * Find & replace null values
    # * Hour window
    # * Target generation
    # * Removal of non categorical fields

    def generate_feature_from_data(self, inp_data):
        try:
            LOGGER.info("Generating features from data")
            LOGGER.info("Input data has the shape %s"%str(inp_data.shape))

            inp_data['start_hour'] = inp_data["Start Date"].apply(mlUtils.get_hour)
            inp_data['start_day'] = inp_data["Start Date"].apply(mlUtils.get_day)

            inp_data['end_hour'] = inp_data["End Date"].apply(mlUtils.get_hour)
            inp_data['end_day'] = inp_data["End Date"].apply(mlUtils.get_day)

            LOGGER.info(inp_data.head())

            #now lets find the count traffic for an hour given a day of the week and terminal
            start_df = inp_data.groupby(by=["start_hour", "start_day", "Start Terminal"]).count().copy()
            start_df = start_df.reset_index()

            LOGGER.info(start_df.head())

            # getting only the required columns
            start_df = start_df.ix[:, ["start_hour", "start_day", "Start Terminal", "Trip ID"]]
            start_df.columns = ["hour", "day", "terminal_code", "trip_id"]
            start_df.head()


            end_df = inp_data.groupby(by=["end_hour", "end_day", "End Terminal"]).count().copy()
            end_df = end_df.reset_index()
            end_df = end_df.ix[:, ["end_hour", "end_day", "End Terminal", "Trip ID"]]
            end_df.columns = ["hour", "day", "terminal_code", "trip_id"]
            LOGGER.info(end_df.head())

            # merge start and end data frames to generate traffic counts for a terminal
            merged_df = start_df.merge(end_df, how="inner", on=["hour", "day", "terminal_code"])


            merged_df["trip_count"] = merged_df["trip_id_x"] + merged_df["trip_id_y"]
            merged_df = merged_df.ix[:, ["hour", "day", "terminal_code", "trip_count"]]

            # generate target variables
            merged_df.trip_count.mean()
            merged_df["target"] = 0
            merged_df.ix[(merged_df.trip_count > merged_df.trip_count.mean()), "target"] = 1

            return merged_df

        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e

    def test_train(self, inp_data):
        try:
            #use this data to train the model and predict
            model = LogisticRegression()
            model.test_train(df=inp_data, target='target', train_split=0.8, test_split=0.2)
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e

    def train(self, inp_data):
        try:
            #use this data to train the model and predict
            model = LogisticRegression()
            model.train(df=inp_data, target='target')
            dir = os.getcwd()
            main_dir = os.path.join(dir, self.main_directory,  self.models_directory, self.name)
            model.persist(main_dir)
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e


if __name__ == '__main__':
    terminal_traffic = TerminalTraffic()
    data = terminal_traffic.get_data()
    terminal_traffic.generate_feature_from_data(inp_data=data)
