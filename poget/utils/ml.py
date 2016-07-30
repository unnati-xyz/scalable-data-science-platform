from delorean import parse
import traceback

from poget import LOGGER

'''

This method is used to get hour
'''
def get_hour(value):

    parsed_date = parse(value).datetime.hour
    return parsed_date


def get_day(value):

    parsed_date = parse(value).datetime.isoweekday()
    return parsed_date


def get_categorical_codes(data_df, categorical_columns):
    try:
        for column in categorical_columns:
            print(column)
            data_df[column] = data_df[column].str.strip()
            data_df[column] = data_df[column].str.lower()
            data_df[column] = data_df[column].astype('category')

        modified_string = '_code'
        categorical_columns_modified = [ column + modified_string for column in categorical_columns]

        data_df[categorical_columns_modified] = data_df[categorical_columns].apply(lambda x: x.cat.codes)

        return data_df

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        raise e

