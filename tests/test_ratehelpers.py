import unittest
import sys
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')
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
            'rate': {
                'value': 0.03
            },
            'spread': {
                'value': 0.03
            }
        }
        curves = {
            'EUR-EONIA': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.02, ore.Actual360()))
        }
        indexes = {
            'EUR-EONIA': ore.Eonia()
        }
        helperConfig = parse(**helperConfig)
        marketConfig = parse(**marketConfig)
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
            'rate': {
                'value': 0.03
            }
        }
        helperConfig = parse(**helperConfig)
        marketConfig = parse(**marketConfig)
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
            'rate': {
                'value': 0.03
            }
        }
        curves = {
            'EUR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.05, ore.Actual360()))
        }
        indexes = {}
        helperConfig = parse(**helperConfig)
        marketConfig = parse(**marketConfig)
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
            'rate': {
                'value': 0.03
            },
            'spread': {
                'value': 0.03
            }
        }
        curves = {
            'EUR-6M': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360()))
        }
        indexes = {
            'EUR-6M': ore.Euribor6M()
        }
        helperConfig = parse(**helperConfig)
        marketConfig = parse(**marketConfig)
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
            'fxPoints': {
                'value': 1
            },
            'fxSpot': {
                'value': 800
            }
        }
        curves = {
            'EUR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360()))
        }
        indexes = {}

        helperConfig = parse(**helperConfig)
        marketConfig = parse(**marketConfig)
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
            "rate": {
                'value': 0.01
            },
            'fxSpot': {
                'value': 800
            },
            "spread": {
                'value': 0.01
            }
        }
        curves = {
            'SOFR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360())),
        }
        indexes = {
            'SOFR': ore.Euribor6M()
        }

        helperConfig = parse(**helperConfig)
        helper = createCrossCcyFixFloatSwapRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.CrossCcyFixFloatSwapHelper)

    def test_createCrossCcyBasisSwapRateHelper(self):
        helperConfig = {
            "tenor": "5Y",
            "calendar": "NullCalendar",
            "settlementDays": 2,
            "endOfMonth": False,
            "convention": "ModifiedFollowing",
            "flatIndex": "SOFR",
            "spreadIndex": "ICP",
            "flatDiscountCurve": "SOFR",
            "spreadDiscountCurve": "CLP_COLLUSD",
            "flatIsDomestic": True
        }
        marketConfig = {           
            'fxSpot': {
                'value': 800
            },
            "spread": {
                'value': 0.01
            }
        }
        curves = {
            'SOFR': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360())),
            'CLP_COLLUSD': ore.YieldTermStructureHandle(ore.FlatForward(2, ore.TARGET(), 0.04, ore.Actual360())),
        }
        indexes = {
            'SOFR': ore.Euribor6M(curves['SOFR']),
            'ICP': ore.IborIndex("ICP", ore.Period("6M"), 0, ore.CLPCurrency(),
                          ore.NullCalendar(), ore.Unadjusted, False, ore.Actual360()),
        }

        helperConfig = parse(**helperConfig)
        helper = createCrossCcyBasisSwapRateHelper(
            helperConfig, marketConfig, curves, indexes)
        self.assertIsInstance(helper, ore.CrossCcyBasisSwapHelper)
