import os
from flask import Flask
from poget.config import configuration as cfg

app = Flask(__name__)

from poget.analytics.ml.logistic_regression import LogisticRegression

from . import routes
