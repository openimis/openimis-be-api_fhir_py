import core

from api_fhir.configurations import GeneralConfiguration


class TimeUtils(object):

    @classmethod
    def now(cls):
        return core.datetime.datetime.now()

    @classmethod
    def str_to_date(cls, str_value):
        date = None
        try:
            date = core.datetime.datetime.strptime(str_value, GeneralConfiguration.get_iso_date_format())
        except ValueError:
            date = core.datetime.datetime.strptime(str_value, GeneralConfiguration.get_iso_datetime_format())
        return date

    class Meta:
        app_label = 'api_fhir'
