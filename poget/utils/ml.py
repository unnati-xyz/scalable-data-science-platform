from delorean import parse

def get_hour(value):

    parsed_date = parse(value).datetime.hour
    return parsed_date

def get_day(value):

    parsed_date = parse(value).datetime.isoweekday()
    return parsed_date

