from unittest import TestCase

from django.core.exceptions import ValidationError

from ..stuff_date import parse_onvolledige_datum

from datetime import date


class UtilsTests(TestCase):

    def test_parse_onvolledige_datum(self):
        self.assertEqual(parse_onvolledige_datum('V20170228'), date(2017, 2, 28))
        self.assertEqual(parse_onvolledige_datum('V20170101'), date(2017, 1, 1))
        self.assertEqual(parse_onvolledige_datum('V12121212'), date(1212, 12, 12))

        self.assertEqual(parse_onvolledige_datum('D201803'), date(2018, 3, 1))
        self.assertEqual(parse_onvolledige_datum('D202001'), date(2020, 1, 1))

        self.assertEqual(parse_onvolledige_datum('M2016',), date(2016, 1, 1))
        self.assertEqual(parse_onvolledige_datum('M2020',), date(2020, 1, 1))

    def test_parse_empty_date(self):
        # TODO: currently 'J' without the year, month and day, will be 1900, 1, 1. Probably this should be changed
        self.assertEqual(parse_onvolledige_datum('J'), date(1900, 1, 1))

    def test_parse_onvolledige_datum_incorrect_dates(self):
        for corrupt_date in (
            'V20170229',  # date does not exists
            'V20171329',  # month does not exists
            'V201712290',  # length too long
            'V2017122',  # length too short

            'D201800',  # month does not exist
            'D20181',  # length too short
            'D2018031',  # length too long
            'D20180311',  # length too long, volledige datum

            'M0000',  # year does not exist
            'M201012',  # too long
            'M20101212',  # too long, full date
            'M207',  # length is 3

            'blabla2',  # incorrect input
            '20170202',  # missing indicator letter
            'C20170202',  # indicator letter is not allowed

            # input with incorrect types
            None,
            20171112,
            (2017, 11, 11),
        ):
            with self.assertRaises(ValidationError):
                parse_onvolledige_datum(corrupt_date)
