from delorean import parse
import traceback

from poget import LOGGER
from poget.analytics.ml.terminal_traffic import TerminalTraffic

def get_hour(value):

    parsed_date = parse(value).datetime.hour
    return parsed_date

def get_day(value):

    parsed_date = parse(value).datetime.isoweekday()
    return parsed_date

def get_categorical_codes(column):
    try:
        column = column.str.strip()
        column = column.str.lower()
        column = column.astype('category')
        return column.apply(lambda x: x.cat.codes)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        raise e

if __name__ == '__main__':
    terminal_traffic = TerminalTraffic()
    data = terminal_traffic.get_data()
    data['Start Station Codes'] = data['Start Station'].apply(get_categorical_codes)
    print(data.head())

