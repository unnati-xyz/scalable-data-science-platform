import traceback
from poget import LOGGER

def complete_task(fileobj):
    try:

        with fileobj.open('w') as f:
            f.write('Done')
    except Exception as e:
        LOGGER.error(traceback.format_exc())
