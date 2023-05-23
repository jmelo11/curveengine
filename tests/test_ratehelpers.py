import sys, os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')

import unittest
from curveengine import *

class TestRateHelpers(unittest.TestCase):

    def test_createOISRateHelper(self):
        helperConfig = {
            'tenor': '1Y',
            'calendar': 'TARGET',
            'convention': 'ModifiedFollowing',
            'settlementDays': 2,
            'endOfMonth': False,
            'paymentLag': 2,
            'fixedLegFrequency': 'Quarterly',
            'fwdStart': '0D',
            'index': 'EUR-EONIA',
            'discountCurve': 'EUR-EONIA'
        }
        marketConfig = {
            'rate': 0.01,
            'spread': 0.0
        }
        curves = {
            'EUR-EONIA': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.02, ore.Actual360()))
        }
        indexes = {
            'EUR-EONIA': ore.Eonia()
        }
        helperConfig = parse(level="test", **helperConfig)
        marketConfig = parse(level="test", **marketConfig)
        helper = createOISRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.OISRateHelper)

    def test_createDepositRateHelper(self):
        helperConfig = {
            'tenor': '1W',
            'calendar': 'TARGET',
            'convention': 'ModifiedFollowing',
            'dayCounter': 'Actual360',
            'settlementDays': 2,
            'endOfMonth': False
        }
        marketConfig = {
            'rate': 0.02
        }
        helperConfig = parse(level="test", **helperConfig)
        marketConfig = parse(level="test", **marketConfig)
        helper = createDepositRateHelper(helperConfig, marketConfig)
        self.assertIsInstance(helper, ore.DepositRateHelper)

    def test_createFixedRateBondHelper(self):
        helperConfig = {
            'calendar': 'TARGET',
            'convention': 'ModifiedFollowing',
            'settlementDays': 2,
            'frequency': 'Semiannual',
            'startDate': '2022-01-01',
            'endDate': '2032-01-01',
            'couponRate': 0.05,
            'couponDayCounter': 'Actual360'
        }
        marketConfig = {            
            'rate': 0.04
        }
        curves = {
            'EUR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.05, ore.Actual360()))
        }
        indexes = {}
        helperConfig = parse(level="test", **helperConfig)
        marketConfig = parse(level="test", **marketConfig)
        helper = createFixedRateBondRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.BondHelper)

    def test_createSwapRateHelper(self):
        helperConfig = {
            'tenor': '5Y',
            'calendar': 'TARGET',
            'convention': 'ModifiedFollowing',
            'fixedLegFrequency': 'Semiannual',
            'dayCounter': 'Actual360',
            'fwdStart': '0D',
            'index': 'EUR-6M',
            'discountCurve': 'EUR-6M'
        }
        marketConfig = {
            'rate': 0.03,
            'spread': 0.0
        }
        curves = {
            'EUR-6M': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360()))
        }
        indexes = {
            'EUR-6M': ore.Euribor6M()
        }
        helperConfig = parse(level="test", **helperConfig)
        marketConfig = parse(level="test", **marketConfig)
        helper = createSwapRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.SwapRateHelper)

    def test_createFxSwapRateHelper(self):
        helperConfig = {
            'fixingDays': 2,
            'calendar': 'TARGET',
            'convention': 'ModifiedFollowing',
            'endOfMonth': False,
            'baseCurrencyAsCollateral': True,
            'discountCurve': 'EUR',
            'tenor': '1Y'
        }
        marketConfig = {
            'fxPoints': 1.1,
            'fxSpot': 1.2
        }
        curves = {
            'EUR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360()))
        }
        indexes = {}

        helperConfig = parse(level="test", **helperConfig)
        marketConfig = parse(level="test", **marketConfig)
        helper = createFxSwapRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.FxSwapRateHelper)

    def test_createCrossCcyFixFloatSwapRateHelper(self):
        helperConfig = {
            "tenor": "2Y",
            "dayCounter": "Actual360",
            "calendar": "NullCalendar",
            "convention": "ModifiedFollowing",
            "endOfMonth": False,
            "settlementDays": 2,
            "discountCurve": "SOFR",
            "index": "SOFR",
            "fixedLegCurrency": "CLP",
            "fwdStart": "0D",
            "fixedLegFrequency": "Semiannual"
        }
        marketConfig = {
            "rate": 0.0695,
            "fxSpot": 786.28,
            "spread": 0.0,
        }
        curves = {
            'SOFR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360())),
        }
        indexes = {
            'SOFR': ore.Euribor6M()
        }

        helperConfig = parse(level="test", **helperConfig)
        helper = createCrossCcyFixFloatSwapRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.CrossCcyFixFloatSwapHelper)
