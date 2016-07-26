import os
import shutil
from pyspark import SparkConf, SparkContext,SQLContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel

from poget import LOGGER


class LogisticRegression:

    def __init__(self):
        # configuring spark
        self.spark_conf = SparkConf()
        self.sc = SparkContext(conf=self.spark_conf)
        self.sql_context = SQLContext(self.sc)

    def test_train(self, df, target, train_split, test_split, regularization=None, num_of_iterations=100):
        try:
            LOGGER.info("Generation logistic regression")

            spark_df = self.sql_context.createDataFrame(df)
            feature_columns = spark_df.columns
            feature_columns.remove(target)

            train, test = spark_df.randomSplit([train_split, test_split], seed=1000000)

            X_train = train.select(*feature_columns).map(lambda x: list(x))
            y_train = train.select(target).map(lambda x: x[0])

            zipped = y_train.zip(X_train)
            train_data = zipped.map(lambda x: LabeledPoint(x[0], x[1]))

            numOfClasses = len(df[target].unique())

            logistic_model = LogisticRegressionWithLBFGS.train(train_data,
                                                               numClasses=numOfClasses, regParam=0,
                                                               regType=regularization, intercept=True,
                                                               iterations=num_of_iterations, validateData=False)

            X_test = test.select(*feature_columns).map(lambda x: list(x))
            y_test = test.select(target).map(lambda x: x[0])

            prediction = X_test.map(lambda lp: (float(logistic_model.predict(lp))))
            prediction_and_label = prediction.zip(y_test)

            LOGGER.info(prediction_and_label.map(lambda labelAndPred: labelAndPred[0] == labelAndPred[1]).mean())
        except Exception as e:
            raise e

    def train(self, df, target, regularization=None, num_of_iterations=100):
        try:
            LOGGER.info("Generation logistic regression")

            spark_df = self.sql_context.createDataFrame(df)
            feature_columns = spark_df.columns
            feature_columns.remove(target)


            X_train = spark_df.select(*feature_columns).map(lambda x: list(x))
            y_train = spark_df.select(target).map(lambda x: x[0])

            zipped = y_train.zip(X_train)
            train_data = zipped.map(lambda x: LabeledPoint(x[0], x[1]))
            numOfClasses = len(df[target].unique())

            logistic_model = LogisticRegressionWithLBFGS.train(train_data,
                                                               numClasses=numOfClasses, regParam=0,
                                                               regType=regularization, intercept=True,
                                                               iterations=num_of_iterations, validateData=False)


            self.model = logistic_model

        except Exception as e:
            raise e


    def persist(self, location):
        try:
            LOGGER.info("Writing the model to location %s"%location)
            data = 'data'
            meta_data = 'metadata'

            data_location = os.path.join(location,data)
            if os.path.exists(data_location):
                LOGGER.info("Removing directory %s"%data_location)
                shutil.rmtree(data_location)

            data_location = os.path.join(location,meta_data)
            if os.path.exists(data_location):
                LOGGER.info("Removing directory %s"%data_location)
                shutil.rmtree(data_location)

            self.model.save(self.sc, location)
        except Exception as e:
            raise e


    def predict(self, df):
        try:
            LOGGER.info("Predicting using random forest")
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
            self.model = LogisticRegressionModel.load(self.sc, location)
        except Exception as e:
            raise e
