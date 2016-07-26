import traceback
import luigi
from luigi.mock import MockTarget

from poget import LOGGER
from poget.utils.luigi import complete_task
from poget.analytics.ml.terminal_traffic import TerminalTraffic


class TerminalTrafficTrainTask(luigi.Task):

    def output(self):
        return MockTarget("terminal-traffic-train-task")

    def run(self):

        try:
            LOGGER.info("starting terminal traffic train task")
            terminal_traffic = TerminalTraffic()
            LOGGER.info("get traffic terminal data")
            data = terminal_traffic.get_data()

            LOGGER.info("generate features for terminal traffic")
            df = terminal_traffic.generate_feature_from_data(inp_data=data)
            LOGGER.info("generate target for terminal traffic")
            df = terminal_traffic.generate_target(df)

            LOGGER.info("train traffic model")
            model = terminal_traffic.train_model(df)
            LOGGER.info("persisting predictive model")
            model.persist(location="poget/data/traffic/")

            complete_task(self.output())

        except Exception:
            LOGGER.error(traceback.format_exc())
