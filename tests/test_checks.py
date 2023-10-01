import unittest
import sys
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')
from curveengine import *


class TestChecks(unittest.TestCase):
    def test_tenor_check(self):
        self.assertRaises(ValueError, checkTenor, '1')
        self.assertRaises(ValueError, checkTenor, 'MD')
        self.assertIsNone(checkTenor('1Y'))
        self.assertIsNone(checkTenor('1W'))
        self.assertIsNone(checkTenor('1D'))
        self.assertIsNone(checkTenor('1M'))
        self.assertIsNone(checkTenor('1M1Y'))

    def test_check_instance(self):
        self.assertRaises(ValueError, checkInstance, 1, str)
        self.assertIsNone(checkInstance(1, int))

    def test_check_is_in_enum(self):
        self.assertRaises(ValueError, checkIsInEnum, '1', ['2', '3'])
        self.assertIsNone(checkIsInEnum('1', ['1', '2']))

    def test_check_dict_structure(self):
        reference = {'a': partial(checkInstance, type=int), 'b': partial(
            checkInstance, type=str)}
        self.assertRaises(KeyError, checkDictStructure, {'a': 1}, reference)
        self.assertRaises(ValueError, checkDictStructure,
                          {'a': 1, 'b': 1}, reference)
        self.assertIsNone(checkDictStructure({'a': 1, 'b': 'test'}, reference))

    def test_ois_check(self):
        goodHelperConfig = {
            "tenor": "1W",
            "dayCounter": "Actual360",
            "calendar": "NullCalendar",
            "convention": "Following",
            "endOfMonth": True,
            "frequency": "Annual",
            "settlementDays": 2,
            "paymentLag": 2,
            "telescopicValueDates": True,
            "index": "SOFR",
            "fixedLegFrequency": "Semiannual",
            "fwdStart": "0D",
            "discountCurve": "SOFR"
        }
        badHelperConfig = {
            "tenor": "1W",
            "dayCounter": "Actual360"
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkOISRateHelper, badHelperConfig)
        self.assertIsNone(checkOISRateHelper(goodHelperConfig))

    def test_deposit_check(self):
        goodHelperConfig = {
            "dayCounter": "Actual360",
            "tenor": "1D",
            "calendar": "NullCalendar",
            "settlementDays": 0,
            "endOfMonth": False,
            "convention": "Unadjusted"
        }
        badHelperConfig = {
            "dayCounter": "Actual360",
            "tenor": "1D",
            "calendar": "Something Invalid",
            "settlementDays": 0,
            "endOfMonth": False,
            "convention": "Unadjusted"
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkDepositRateHelper, badHelperConfig)
        self.assertIsNone(checkDepositRateHelper(goodHelperConfig))

    def test_swap_check(self):
        goodHelperConfig = {
            "tenor": "2Y",
            "dayCounter": "Thirty360",
            "calendar": "NullCalendar",
            "frequency": "Semiannual",
            "settlementDays": 2,
            "discountCurve": "SOFR",
            "index": "LIBOR3M",
            "endOfMonth": False,
            "convention": "Unadjusted",
            "fixedLegFrequency": "Semiannual",
            "fwdStart": "0D"
        }

        badHelperConfig = {
            "dayCounter": "Actual360",
            "tenor": "1Y",
            "calendar": "NullCalendar",
            "fixedLegFrequency": "Semiannual",
            "fixedLegConvention": "Unadjusted",
            "fixedLegDayCounter": "Actual360",
            "index": "USDLibor",
            "floatingLegFrequency": "Quarterly",
            "floatingLegConvention": "ModifiedFollowing",
            "floatingLegDayCounter": "Actual360",
            "settlementDays": 2,
            "fixedLegTenor": "1Y",
            "floatingLegTenor": "1Y",
            "endOfMonth": False,
            "something": "invalid"
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkSwapRateHelper, badHelperConfig)
        self.assertIsNone(checkSwapRateHelper(goodHelperConfig))

    def test_fixed_rate_bond_check(self):
        goodHelperConfig = {
            "calendar": "NullCalendar",
            "convention": "Following",
            "settlementDays": 2,
            "couponDayCounter": "Actual360",
            "couponRate": 0.05,
            "frequency": "Annual",
            "tenor": "2Y"  # needed if start date and end date are not provided
        }
        goodHelperConfig2 = {
            "calendar": "NullCalendar",
            "convention": "Following",
            "settlementDays": 2,
            "couponDayCounter": "Actual360",
            "couponRate": 0.05,
            "frequency": "Annual",
            "startDate": "2019-01-01",
            "endDate": "2020-01-01"
        }

        badHelperConfig = {
            "dayCounter": "ActualActual",
            "tenor": "1Y",
            "calendar": "NullCalendar",
            "settlementDays": 2,
            "endOfMonth": False,
            "convention": "Unadjusted",
            "frequency": "Semiannual",
            "discountCurve": "SOFR",
            "faceAmount": 100,
            "maturity": "2020-01-01",
            "coupon": 0.05,
            "issueDate": "2019-01-01",
            "something": "invalid"
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkFixedRateBondRateHelper, badHelperConfig)
        self.assertIsNone(checkFixedRateBondRateHelper(goodHelperConfig))
        self.assertIsNone(checkFixedRateBondRateHelper(goodHelperConfig2))

    def test_fxswap_check(self):
        goodHelperConfig = {
            "calendar": "NullCalendar",
            "fixingDays": 0,
            "endOfMonth": False,
            "baseCurrencyAsCollateral": False,
            "convention": "Following",
            "discountCurve": "CLP_COLLUSD",
            "endDate": "2023-04-09",
            "tenor": "1Y",  # need if no end date is provided
            "settlementDays": 0
        }
        badHelperConfig = {
            "spotFx": 1.0,
            "tenor": "1Y",
            "calendar": "NullCalendar",
            "settlementDays": 2,
            "endOfMonth": False,
            "convention": "Unadjusted",
            "forwardPoints": 0.01,
            "swapType": "Something Invalid"
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkFxSwapRateHelper, badHelperConfig)
        self.assertIsNone(checkFxSwapRateHelper(goodHelperConfig))

    def test_rateHelper_check(self):

        h1 = {
            "helperType": "Something Invalid"
        }

        h2 = {
            "helperType": "OIS",
            "helperConfig": {

            },
            "marketConfig": {

            }
        }

        h3 = {
            "helperType": "OIS",
            "helperConfig": {
                "tenor": "1W",
                "dayCounter": "Actual360",
                "calendar": "NullCalendar",
                "convention": "Following",
                "endOfMonth": True,
                "frequency": "Annual",
                "settlementDays": 2,
                "paymentLag": 2,
                "telescopicValueDates": True,
                "index": "SOFR",
                "fixedLegFrequency": "Semiannual",
                "fwdStart": "0D"
            },
            "marketConfig": {

            }
        }

        h4 = {
            "helperType": "OIS",
            "helperConfig": {
                "tenor": "1W",
                "dayCounter": "Actual360",
                "calendar": "NullCalendar",
                "convention": "Following",
                "endOfMonth": True,
                "frequency": "Annual",
                "settlementDays": 2,
                "paymentLag": 2,
                "telescopicValueDates": True,
                "index": "SOFR",
                "fixedLegFrequency": "Semiannual",
                "fwdStart": "0D",
                "discountCurve": "SOFR"
            },
            "marketConfig": {
                "rate": {
                    "value": 0.01,
                },
                "spread": {
                    "value": 0.0,
                }
            }
        }

        self.assertRaises(ConfigurationError,
                          checkRateHelper, h1, 0)
        self.assertRaises(ConfigurationError,
                          checkRateHelper, h2, 0)
        self.assertRaises(ConfigurationError,
                          checkRateHelper, h3, 0)
        self.assertIsNone(checkRateHelper(h4, 0))

    def test_index_check(self):

        h1 = {
            "indexType": "OvernightIndex",
            "tenor": "1D",
            "fixingDays": 0,
            "calendar": "NullCalendar",
            "endOfMonth": False,
            "convention": "Unadjusted"
        }

        h2 = {
            "indexType": "OvernightIndex",
            "tenor": "1D",
            "dayCounter": "Actual360",
            "currency": "USD",
            "fixingDays": 0,
            "calendar": "NullCalendar",
            "endOfMonth": False,
            "convention": "Unadjusted"
        }

        self.assertRaises(ConfigurationError,
                          checkIndex, h1)
        self.assertIsNone(checkIndex(h2))

    def test_market_config_check(self):

        h1 = {
            "rate": {}
        }

        h2 = {
            "rate": {
                "value": 0.01
            }
        }

        self.assertRaises(ConfigurationError,
                          checkMarketConfig, h1, HelperType.Deposit)
        self.assertIsNone(checkMarketConfig(h2,  HelperType.Deposit))
    # TODO: Add more tests for the other rate helpers
    # checkTenorBasisRateHelper

    def test_tenor_basis_check(self):
        goodHelperConfig = {
            "tenor": "3M",
            "longIndex": "LIBOR3M",
            "shortIndex": "LIBOR1M",
            "discountCurve": "SOFR",
            "spreadOnShort": True
        }
        badHelperConfig = {
            "tenor": "3M",
            "spreadOnShort": True
        }

        self.assertRaises(RateHelperConfigurationError,
                          checkTenorBasisSwapRateHelper, badHelperConfig)
        self.assertIsNone(checkTenorBasisSwapRateHelper(goodHelperConfig))

    def test_xccy_basis_check(self):
        goodHelperConfig = {
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
        badHelperConfig = {
            "tenor": "3M",
            "calendar": "NullCalendar",
            "settlementDays": 2,
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkCrossCcyBasisSwapRateHelper, badHelperConfig)
        self.assertIsNone(checkCrossCcyBasisSwapRateHelper(goodHelperConfig))

    def test_xccy_fix_float_check(self):
        goodHelperConfig = {
            "tenor": "2Y",
            "dayCounter": "Actual360",
            "calendar": "NullCalendar",
            "convention": "ModifiedFollowing",
            "endOfMonth": False,
            "settlementDays": 2,
            "discountCurve": "CLP_COLLUSD",
            "index": "ICP",
            "fixedLegCurrency": "CLF",
            "fwdStart": "0D",
            "fixedLegFrequency": "Semiannual"
        }
        badHelperConfig = {
            "tenor": "2Y",
            "dayCounter": "Actual360",
            "calendar": "NullCalendar",
            "index": "ICP",
            "fixedLegCurrency": "CLF",
            "fwdStart": "0D",
            "fixedLegFrequency": "Semiannual"
        }
        self.assertRaises(RateHelperConfigurationError,
                          checkCrossCcyFixFloatSwapRateHelper, badHelperConfig)
        self.assertIsNone(
            checkCrossCcyFixFloatSwapRateHelper(goodHelperConfig))

    def test_piecewise_check(self):
        c1 = {
            "curveType": "Something Invalid"
        }

        c2 = {
            "curveType": "Piecewise",
            "dayCounter": "Actual360",
            "enableExtrapolation": True,
            "rateHelpers": [

            ]
        }

        c3 = {
            "curveType": "Piecewise",
            "dayCounter": "Actual360",
            "enableExtrapolation": True,
            "currency": "USD",
            "rateHelpers": [
                {
                    "helperType": "OIS",
                    "helperConfig": {
                        "tenor": "1W",
                        "dayCounter": "Actual360",
                        "calendar": "NullCalendar",
                        "convention": "Following",
                        "endOfMonth": True,
                        "frequency": "Annual",
                        "settlementDays": 2.0,
                        "paymentLag": 2,
                        "telescopicValueDates": True,
                        "index": "SOFR",
                        "fixedLegFrequency": "Semiannual",
                        "fwdStart": "0D",
                        "discountCurve": "SOFR"
                    },
                    "marketConfig": {
                        "rate": {
                            "value": 0.01,
                        },
                        "spread": {
                            "value": 0.0,
                        }
                    }
                }
            ]
        }

        self.assertRaises(ConfigurationError,
                          checkPiecewiseCurve, c1)
        self.assertRaises(ConfigurationError,
                          checkPiecewiseCurve, c2)
        self.assertIsNone(checkPiecewiseCurve(c3))

    def test_discount_check(self):
        c1 = {
            "curveType": "Something Invalid"
        }

        c2 = {
            "curveType": "Discount",
            "dayCounter": "Actual360",
            "enableExtrapolation": True,
            "rateHelpers": [

            ]
        }

        c3 = {
            "curveType": "Discount",
            "dayCounter": "Actual360",
            "enableExtrapolation": True,
            "currency": "USD",
            "nodes": [
                {
                    "date": "2020-01-01",
                    "value": 0.99
                }
            ]
        }

        self.assertRaises(ConfigurationError,
                          checkDiscountCurve, c1)
        self.assertRaises(ConfigurationError,
                          checkDiscountCurve, c2)
        self.assertIsNone(checkDiscountCurve(c3))

    def test_curve_check(self):
        c1 = {
            "curveName": "Something Invalid",
            "curveType": "Something Invalid"
        }

        c2 = {
            "curveName": "Test",
            "curveConfig": {
                "curveType": "Curve",
                "dayCounter": "Actual360",
                "enableExtrapolation": True,
                "rateHelpers": []
            },
            "curveIndex": {}
        }

        c3 = {
            "curveName": "Test",
            "curveConfig": {
                "curveType": "Piecewise",
                "dayCounter": "Actual360",
                "enableExtrapolation": True,
                "currency": "USD",
                "rateHelpers": [{
                    "helperType": "OIS",
                    "helperConfig": {
                        "tenor": "1W",
                        "dayCounter": "Actual360",
                        "calendar": "NullCalendar",
                        "convention": "Following",
                        "endOfMonth": True,
                        "frequency": "Annual",
                        "settlementDays": 2,
                        "paymentLag": 2,
                        "telescopicValueDates": True,
                        "index": "SOFR",
                        "fixedLegFrequency": "Semiannual",
                        "fwdStart": "0D",
                        "discountCurve": "SOFR"
                    },
                    "marketConfig": {
                        "rate": {
                            "value": 0.01,
                        },
                        "spread": {
                            "value": 0.0,
                        }
                    }
                }]
            },
            "curveIndex": {
                "indexType": "IborIndex",
                "tenor": "6M",
                "dayCounter": "Actual360",
                "currency": "CLP",
                "fixingDays": 0,
                "calendar": "NullCalendar",
                "endOfMonth": False,
                "convention": "Unadjusted"
            }
        }

        self.assertRaises(ConfigurationError,
                          checkCurve, c1, 0)
        self.assertRaises(ConfigurationError,
                          checkCurve, c2, 0)
        self.assertIsNone(checkCurve(c3, 0))
