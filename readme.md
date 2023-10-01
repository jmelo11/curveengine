# CurveEngine

A simple curve bootstrapping tool. It uses ORE as backend and parses configuration files (see example below) and transform them into QL/ORE objects.

## Documentation

Documentation is available at [https://jmelo11.github.io/curveenginedocs/](https://jmelo11.github.io/curveenginedocs/)

## Build

For building the project, you need to have cmake installed. Then, run the following commands:

```cmd
python -m build
```

## Example

For a more detail example, visit the example folder.

```json
{
    "refDate": "2023-02-14",
    "curves": [
        {
            "curveName": "SOFR",
            "curveConfig": {
                "curveType": "Piecewise",
                "dayCounter": "Actual360",
                "enableExtrapolation": true,
                "rateHelpers": [
                    {
                        "helperType": "Deposit",
                        "helperConfig": {
                            "dayCounter": "Actual360",
                            "tenor": "1D",
                            "calendar": "NullCalendar",
                            "settlementDays": 0,
                            "endOfMonth": false,
                            "convention": "Unadjusted"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.0455,
                                "ticker": "SOFRRATE CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "1W",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.045555000000000005,
                                "ticker": "USOSFR1Z CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "2W",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.045568,
                                "ticker": "USOSFR2Z CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "1M",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.04564,
                                "ticker": "USOSFRA CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "3M",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.047723,
                                "ticker": "USOSFRC CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "6M",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.050135,
                                "ticker": "USOSFRF CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "12M",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.051856,
                                "ticker": "USOSFR1 CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "3Y",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.042443,
                                "ticker": "USOSFR3 CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "5Y",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.037866,
                                "ticker": "USOSFR5 CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "7Y",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.035910000000000004,
                                "ticker": "USOSFR7 CURNCY"
                            }
                        }
                    },
                    {
                        "helperType": "OIS",
                        "helperConfig": {
                            "tenor": "10Y",
                            "dayCounter": "Actual360",
                            "calendar": "NullCalendar",
                            "convention": "Following",
                            "endOfMonth": true,
                            "frequency": "Annual",
                            "settlementDays": 2,
                            "paymentLag": 2,
                            "telescopicValueDates": true,
                            "index": "SOFR",
                            "fixedLegFrequency": "Semiannual",
                            "fwdStart": "0D"
                        },
                        "marketConfig": {
                            "rate": {
                                "value": 0.03464,
                                "ticker": "USOSFR10 CURNCY"
                            }
                        }
                    }
                ]
            },
            "curveIndex": {
                "indexType": "OvernightIndex",
                "tenor": "1D",
                "dayCounter": "Actual360",
                "currency": "USD",
                "fixingDays": 0,
                "calendar": "NullCalendar",
                "endOfMonth": false,
                "convention": "Unadjusted"
            }
        }
    ]
}
```
