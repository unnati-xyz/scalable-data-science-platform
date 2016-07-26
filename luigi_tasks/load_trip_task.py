import traceback
import luigi
from luigi.mock import MockTarget

from poget import LOGGER
from poget.utils.luigi import complete_task
from poget.analytics.data_load.bay_bike_share import BayBikeShare

class LoadTripTask(luigi.Task):

    def output(self):
        return MockTarget("load-trip-task")

    def run(self):

        try:
            LOGGER.info("starting load trip task")
            bike_share = BayBikeShare()
            bike_share.load_data()

            LOGGER.info("Load trip data complete")
            complete_task(self.output())

        except Exception as e:
            LOGGER.error(traceback.format_exc())
