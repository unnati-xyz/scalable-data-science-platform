from flask import Flask
from poget.config import configuration as cfg

app = Flask(__name__)

from poget.analytics.ml.terminal_traffic import TerminalTraffic

terminal_traffic = TerminalTraffic()

from . import routes
