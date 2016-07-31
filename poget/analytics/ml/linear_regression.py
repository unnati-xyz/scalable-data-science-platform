import os
import shutil
from pyspark import SparkConf, SparkContext,SQLContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from decimal import Decimal

from poget import LOGGER


class LinearRegression:

    def __init__(self):
        # configuring spark
        self.spark_conf = SparkConf()
        self.sc = SparkContext(conf=self.spark_conf)
        self.sql_context = SQLContext(self.sc)

    def test_train(self, df, target, train_split, test_split):
        try:
            LOGGER.info("Generation linear regression")

            spark_df = self.sql_context.createDataFrame(df)
            feature_columns = spark_df.columns
            feature_columns.remove(target)

            train, test = spark_df.randomSplit([train_split, test_split], seed=1000000)

            X_train = train.select(*feature_columns).map(lambda x: list(x))
            y_train = train.select(target).map(lambda x: x[0])

            zipped = y_train.zip(X_train)
            train_data = zipped.map(lambda x: LabeledPoint(x[0], x[1]))

            linear_model = LinearRegressionWithSGD.train(train_data, intercept=True)

            X_test = test.select(*feature_columns).map(lambda x: list(x))
            y_test = test.select(target).map(lambda x: x[0])

            prediction = X_test.map(lambda lp: (float(linear_model.predict(lp))))
            label_and_prediction = prediction.zip(y_test)
            val = label_and_prediction.map(lambda vp: (Decimal(vp[0]) - Decimal(vp[1])) ** 2).reduce(lambda x, y: x + y)/label_and_prediction.count()

            LOGGER.info(val)
        except Exception as e:
            raise e

    def train(self, df, target):
        try:
            LOGGER.info("Generation linear regression")

            spark_df = self.sql_context.createDataFrame(df)
            feature_columns = spark_df.columns
            feature_columns.remove(target)


            X_train = spark_df.select(*feature_columns).map(lambda x: list(x))
            y_train = spark_df.select(target).map(lambda x: x[0])

            zipped = y_train.zip(X_train)
            train_data = zipped.map(lambda x: LabeledPoint(x[0], x[1]))

            linear_model = LinearRegressionWithSGD.train(train_data, intercept=True)

            self.model = linear_model

        except Exception as e:
            raise e


    def persist(self, location):
        try:
            LOGGER.info("Writing the model to location %s"%location)
            data = 'data'
            meta_data = 'metadata'

            data_location = os.path.join(location, data)
            if os.path.exists(data_location):
                LOGGER.info("Removing directory %s"%data_location)
                shutil.rmtree(data_location)

            data_location = os.path.join(location, meta_data)
            if os.path.exists(data_location):
                LOGGER.info("Removing directory %s"%data_location)
                shutil.rmtree(data_location)

            self.model.save(self.sc, location)
        except Exception as e:
            raise e


    def predict(self, df):
        try:
            LOGGER.info("Predicting using linear regression")
            spark_df = self.sql_context.createDataFrame(df)
            feature_columns = spark_df.columns
            inp_data = spark_df.select(*feature_columns).map(lambda x: list(x))
            inp_data = spark_df.map(lambda x: list(x))
            result = self.model.predict(inp_data.map(lambda x: x)).collect()
            LOGGER.info("Predicted output is %s"%str(result))
            return result

        except Exception as e:
            raise e

    def load(self, location):
        try:
            self.model = LinearRegressionWithSGD.load(self.sc, location)
        except Exception as e:
            raise e
