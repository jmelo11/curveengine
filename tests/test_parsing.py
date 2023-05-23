import sys, os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')

import unittest
from curveengine import *


class TestParsing(unittest.TestCase):
    def test_parse_compounding(self):
        self.assertEqual(parseCompounding('Simple'), ore.Simple)
        self.assertEqual(parseCompounding('Compounded'), ore.Compounded)
        self.assertEqual(parseCompounding('Continuous'), ore.Continuous)
        with self.assertRaises(Exception):
            parseCompounding('unknown')

    def test_parse_frequency(self):
        self.assertEqual(parseFrequency('Once'), ore.Once)
        self.assertEqual(parseFrequency('Annual'), ore.Annual)
        self.assertEqual(parseFrequency('Semiannual'), ore.Semiannual)
        self.assertEqual(parseFrequency(
            'EveryFourthMonth'), ore.EveryFourthMonth)
        self.assertEqual(parseFrequency('Quarterly'), ore.Quarterly)
        self.assertEqual(parseFrequency('Bimonthly'), ore.Bimonthly)
        self.assertEqual(parseFrequency('Monthly'), ore.Monthly)
        self.assertEqual(parseFrequency(
            'EveryFourthWeek'), ore.EveryFourthWeek)
        self.assertEqual(parseFrequency('Biweekly'), ore.Biweekly)
        self.assertEqual(parseFrequency('Weekly'), ore.Weekly)
        self.assertEqual(parseFrequency('Daily'), ore.Daily)
        with self.assertRaises(Exception):
            parseFrequency('unknown')

    def test_parse_day_counter(self):
        self.assertIsInstance(parseDayCounter('Actual365'), ore.Actual365Fixed)
        self.assertIsInstance(parseDayCounter('Actual360'), ore.Actual360)
        self.assertIsInstance(parseDayCounter('Thirty360'), ore.Thirty360)
        with self.assertRaises(Exception):
            parseDayCounter('unknown')

    def test_parse_calendar(self):
        self.assertIsInstance(parseCalendar('TARGET'), ore.TARGET)
        self.assertIsInstance(parseCalendar('UnitedStates'), ore.UnitedStates)
        self.assertIsInstance(parseCalendar('Chile'), ore.Chile)
        self.assertIsInstance(parseCalendar('Brazil'), ore.Brazil)
        self.assertIsInstance(parseCalendar('NullCalendar'), ore.NullCalendar)
        with self.assertRaises(Exception):
            parseCalendar('unknown')

    def test_parse_business_day_convention(self):
        self.assertEqual(parseBusinessDayConvention(
            'Following'), ore.Following)
        self.assertEqual(parseBusinessDayConvention(
            'ModifiedFollowing'), ore.ModifiedFollowing)
        self.assertEqual(parseBusinessDayConvention(
            'Preceding'), ore.Preceding)
        self.assertEqual(parseBusinessDayConvention(
            'ModifiedPreceding'), ore.ModifiedPreceding)
        self.assertEqual(parseBusinessDayConvention(
            'Unadjusted'), ore.Unadjusted)
        self.assertEqual(parseBusinessDayConvention(
            'HalfMonthModifiedFollowing'), ore.HalfMonthModifiedFollowing)
        with self.assertRaises(Exception):
            parseBusinessDayConvention('unknown')

    def test_parse_time_unit(self):
        self.assertEqual(parseTimeUnit('Days'), ore.Days)
        self.assertEqual(parseTimeUnit('Weeks'), ore.Weeks)
        self.assertEqual(parseTimeUnit('Months'), ore.Months)
        self.assertEqual(parseTimeUnit('Years'), ore.Years)
        with self.assertRaises(Exception):
            parseTimeUnit('unknown')

    def test_parse_date_generation_rule(self):
        self.assertEqual(parseDateGenerationRule(
            'Backward'), ore.DateGeneration.Backward)
        self.assertEqual(parseDateGenerationRule(
            'Forward'), ore.DateGeneration.Forward)
        self.assertEqual(parseDateGenerationRule(
            'Zero'), ore.DateGeneration.Zero)
        self.assertEqual(parseDateGenerationRule(
            'ThirdWednesday'), ore.DateGeneration.ThirdWednesday)
        self.assertEqual(parseDateGenerationRule(
            'Twentieth'), ore.DateGeneration.Twentieth)
        self.assertEqual(parseDateGenerationRule(
            'TwentiethIMM'), ore.DateGeneration.TwentiethIMM)
        self.assertEqual(parseDateGenerationRule(
            'OldCDS'), ore.DateGeneration.OldCDS)

        with self.assertRaises(Exception):
            parseDateGenerationRule('unknown')

    def test_parse_date(self):
        self.assertEqual(parseDate('today'), ore.Date.todaysDate())
        self.assertEqual(parseDate('2019-01-01'), ore.Date(1, 1, 2019))
        with self.assertRaises(Exception):
            parseDate('unknown')

    def test_parse_period(self):
        self.assertEqual(parsePeriod('1D'), ore.Period(1, ore.Days))
        self.assertEqual(parsePeriod('1W'), ore.Period(1, ore.Weeks))
        self.assertEqual(parsePeriod('1M'), ore.Period(1, ore.Months))
        self.assertEqual(parsePeriod('1Y'), ore.Period(1, ore.Years))
        with self.assertRaises(Exception):
            parsePeriod('unknown')

    def test_parse_currency(self):
        self.assertIsInstance(parseCurrency('USD'), ore.USDCurrency)
        self.assertIsInstance(parseCurrency('EUR'), ore.EURCurrency)
        self.assertIsInstance(parseCurrency('CLP'), ore.CLPCurrency)
        self.assertIsInstance(parseCurrency('BRL'), ore.BRLCurrency)
        self.assertIsInstance(parseCurrency('CLF'), ore.CLFCurrency)
        self.assertIsInstance(parseCurrency('JPY'), ore.JPYCurrency)
        self.assertIsInstance(parseCurrency('CHF'), ore.CHFCurrency)
        self.assertIsInstance(parseCurrency('COP'), ore.COPCurrency)
        self.assertIsInstance(parseCurrency('MXN'), ore.MXNCurrency)
        self.assertIsInstance(parseCurrency('PEN'), ore.PENCurrency)
        with self.assertRaises(Exception):
            parseCurrency('unknown')

    def test_parse_kwargs_1(self):
        kwargs = {
            'date': '2023-04-13',
            'currency': 'USD',
            'compounding': 'Compounded',
            'frequency': 'Semiannual',
            'dayCounter': 'Actual365'
        }
        expected_result = {
            'date': ore.Date(13, ore.April, 2023),
            'currency': ore.USDCurrency(),
            'compounding': ore.Compounded,
            'frequency': ore.Semiannual,
            'dayCounter': ore.Actual365Fixed()
        }
        self.assertEqual(parse(**kwargs), expected_result)

    def test_parse_kwargs_2(self):
        kwargs = {
            'startDate': '2023-01-01',
            'endDate': '2023-12-31',
            'paymentFrequency': 'Monthly',
            'couponRate': 0.05,
            'dayCounter': 'Actual360',
            'convention': 'ModifiedFollowing',
            'calendar': 'TARGET'
        }
        expected_result = {
            'startDate': ore.Date(1, ore.January, 2023),
            'endDate': ore.Date(31, ore.December, 2023),
            'paymentFrequency': ore.Monthly,
            'couponRate': 0.05,
            'dayCounter': ore.Actual360(),
            'convention': ore.ModifiedFollowing,
            'calendar': ore.TARGET()
        }
        self.assertEqual(parse(**kwargs), expected_result)

    def test_parse_kwargs_3(self):
        kwargs = {
            'index': 'USD-LIBOR-3M',
            'fixingDays': 2,
            'calendar': 'TARGET',
            'dayCounter': 'Actual360'
        }
        expected_result = {
            'index': 'USD-LIBOR-3M',
            'fixingDays': 2,
            'calendar': ore.TARGET(),
            'dayCounter': ore.Actual360()
        }
        self.assertEqual(parse(**kwargs), expected_result)
