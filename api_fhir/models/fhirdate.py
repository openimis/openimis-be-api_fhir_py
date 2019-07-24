import re


class FHIRDate(object):

    date = None
    _datetime_regex = '([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[' \
                      '0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]+)?(Z|(\\+|-)((0[0-9]|1[0-3]):[' \
                      '0-5][0-9]|14:00)))?)?)?'
    _date_regex = '([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1]))?)?'
    _time_regex = '([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]+)?'

    @classmethod
    def validate_type(cls, value):
        valid = False
        if value and isinstance(value, str):
            if re.search(cls._datetime_regex, value):
                valid = True
            if not valid and re.search(cls._date_regex, value):
                valid = True
            if not valid and re.search(cls._time_regex, value):
                valid = True
        return valid
