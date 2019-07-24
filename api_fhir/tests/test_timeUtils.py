from unittest import TestCase

import core
import dateutil

from api_fhir.utils import TimeUtils


class TimeUtilsTestCase(TestCase):

    __OFFSET_IN_SECONDS = 3600

    def test_str_converting_datetime(self):
        str_value = "2010-11-16T15:22:01"
        expected = core.datetime.datetime(2010, 11, 16, 15, 22, 1, 0)
        actual = TimeUtils.str_to_date(str_value)
        self.assertEqual(expected, actual)

    def test_str_converting_datetime_with_time_zone(self):
        str_value = "2010-11-16T15:22:01+01:00"
        expected = core.datetime.datetime(2010, 11, 16, 15, 22, 1, 0,
                                          tzinfo=dateutil.tz.tzoffset(None, self.__OFFSET_IN_SECONDS))
        actual = TimeUtils.str_to_date(str_value)
        self.assertEqual(expected, actual)

    def test_str_converting_date(self):
        str_value = "2010-11-16"
        expected = core.datetime.date(2010, 11, 16)
        actual = TimeUtils.str_to_date(str_value)
        self.assertEqual(expected, actual)
