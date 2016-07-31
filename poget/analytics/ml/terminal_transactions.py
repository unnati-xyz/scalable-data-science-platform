import traceback
import json
import pandas as pd
from poget.utils.db import DBConn
import poget.utils.ml as mlUtils
from poget import LOGGER

from poget.analytics.ml.linear_regression import LinearRegression


# ## Hypothesis 2
#
# Given a time slot and terminal code, predict number of transactions
#
# ##
class TerminalTransactions:

    def __init__(self):
        self.name = ''
        self.main_directory = 'poget'
        self.models_directory = 'models'

    def get_data(self):
        try:
            LOGGER.info("Howdy data cruncher")

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
            LOGGER.info("What features do we need")

        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e

    def get_features_for_prediction(self, data):

        try:
            LOGGER.info("I can predict")
        except Exception:
            LOGGER.error(traceback.format_exc())
            raise

    def train_test_model(self, df):
        try:
            LOGGER.info("Train and test people, train and test")
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            raise e

    def train_model(self, df):
        try:
            LOGGER.info("I love machine learning")
        except Exception as e:
            LOGGER.error(traceback.format_exc())


if __name__ == '__main__':
    terminal_transactions = TerminalTransactions()
    data = terminal_transactions.get_data()
    df = terminal_transactions.generate_feature_from_data(inp_data=data)
    terminal_transactions.train_test_model(df=df)
