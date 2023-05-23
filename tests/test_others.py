import sys, os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')

import unittest
from curveengine import *


class TestCreateOvernightIndex(unittest.TestCase):

    def test_create_overnight_index(self):
        # Set up input parameters for the function
        name = 'USDLibor'
        indexConfig = {
            'dayCounter': ore.Actual360(),
            'currency': ore.USDCurrency(),
            'calendar': ore.UnitedStates(ore.UnitedStates.GovernmentBond),
            'fixingDays': 2
        }
        handle = ore.YieldTermStructureHandle(
            ore.FlatForward(0, ore.TARGET(), 0.01, ore.Actual360()))

        # Call the function to create an overnight index
        index = createOvernightIndex(name, indexConfig, handle)

        # Assert that the overnight index is created correctly
        self.assertEqual(index.name(), 'USDLiborSN Actual/360')
        self.assertEqual(index.dayCounter(), indexConfig['dayCounter'])
        self.assertEqual(index.currency(), indexConfig['currency'])
        self.assertEqual(index.fixingCalendar(), indexConfig['calendar'])
        self.assertEqual(index.fixingDays(), indexConfig['fixingDays'])

    def test_create_ibor_index(self):
        index_config = {
            'dayCounter': ore.Actual360(),
            'currency': ore.USDCurrency(),
            'calendar': ore.UnitedStates(ore.UnitedStates.GovernmentBond),
            'fixingDays': 2,
            'tenor': ore.Period(3, ore.Months),
            'endOfMonth': False,
            'convention': ore.ModifiedFollowing
        }
        handle = ore.YieldTermStructureHandle()
        index = createIborIndex('USDLibor', index_config, handle)

        self.assertEqual(index.name(), 'USDLibor3M Actual/360')
        self.assertEqual(index.fixingDays(), 2)
        self.assertEqual(index.tenor(), ore.Period(3, ore.Months))
        self.assertEqual(index.currency(), ore.USDCurrency())
        self.assertEqual(index.fixingCalendar(), ore.UnitedStates(
            ore.UnitedStates.GovernmentBond))
        self.assertEqual(index.businessDayConvention(), ore.ModifiedFollowing)
        self.assertEqual(index.endOfMonth(), False)
        self.assertEqual(index.dayCounter(), ore.Actual360())

    def test_getDependencyList(self):
        data = {
            "curves": [
                {
                    "curveName": "DiscountCurve",
                    "curveConfig": {
                        "curveType": "Piecewise",
                        "rateHelpers": [
                            {
                                "helperType": "OISRateHelper",
                                "name": "USD-6M",
                                "helperConfig": {
                                    "index": "USD-LIBOR-6M",
                                    "discountCurve": "DiscountCurve"
                                },
                                "marketData": {
                                    "rate": 0.01
                                }
                            }
                        ]
                    }
                },
                {
                    "curveName": "CollateralCurve",
                    "curveConfig": {
                        "curveType": "Piecewise",
                        "rateHelpers": [
                            {
                                "helperType": "OIS",
                                "name": "USD-3M",
                                "helperConfig": {
                                    "index": "USD-LIBOR-3M",
                                    "discountCurve": "DiscountCurve"
                                },
                                "marketData": {
                                    "rate": 0.015
                                }
                            },
                            {
                                "helperType": "OIS",
                                "name": "USD-1M",
                                "helperConfig": {
                                    "index": "USD-LIBOR-1M",
                                    "discountCurve": "DiscountCurve"
                                },
                                "marketData": {
                                    "rate": 0.012
                                }
                            }
                        ]
                    }
                },
                {
                    "curveName": "RiskFreeCurve",
                    "curveConfig": {
                        "curveType": "Discount",
                        "nodes":  [
                            {
                                "date": "2020-01-01",
                                "value": 0.9
                            }
                        ]
                    }
                }
            ]
        }

        expected_dependencies = {'DiscountCurve': {'USD-LIBOR-6M', 'DiscountCurve'}, 'CollateralCurve': {
            'USD-LIBOR-3M', 'USD-LIBOR-1M', 'DiscountCurve'}, 'RiskFreeCurve': set()}

        result = getDependencyList(data)
        self.assertEqual(result, expected_dependencies)

    def test_topologicalSort(self):
        dependencies = {
            "a": {"b", "c"},
            "b": {"d"},
            "c": {"d", "e"},
            "d": set(),
            "e": {"d"}
        }

        expected_sort = ["d", "b", "e", "c", "a"]

        self.assertEqual(topologicalSort(dependencies), expected_sort)
