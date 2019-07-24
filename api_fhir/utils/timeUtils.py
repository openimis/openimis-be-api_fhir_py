import core
from dateutil import parser


class TimeUtils(object):

    @classmethod
    def now(cls):
        return core.datetime.datetime.now()

    @classmethod
    def date(cls):
        return core.datetime.datetime.date(cls.now())

    @classmethod
    def str_to_date(cls, str_value):
        py_date = parser.parse(str_value)
        return core.datetime.datetime.from_ad_datetime(py_date)
