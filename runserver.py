from poget.api import app
from poget.config import configuration as cfg
from poget import API_LOGGER as LOGGER

def str2bool(str):
    return str.upper() in ["TRUE", "YES", "T", "1"]

host=cfg["flask_host"]
port=cfg["flask_port"]
debug=str2bool(cfg["flask_debug"])

LOGGER.info("starting server on host %s port %s"%(host, port))
app.run(host=host, port=port, debug=debug)
