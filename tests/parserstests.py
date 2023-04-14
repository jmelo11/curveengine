from parsing.parsers import *


def testParseCompounding():
    assert parseCompounding('Simple') == ore.Simple
    assert parseCompounding('Compounded') == ore.Compounded
    assert parseCompounding('Continuous') == ore.Continuous
    try:
        parseCompounding('unknown')
        assert False
    except Exception as e:
        assert True


def testParseFrequency():
    assert parseFrequency('Once') == ore.Once
    assert parseFrequency('Annual') == ore.Annual
    assert parseFrequency('Semiannual') == ore.Semiannual
    assert parseFrequency('EveryFourthMonth') == ore.EveryFourthMonth
    assert parseFrequency('Quarterly') == ore.Quarterly
    assert parseFrequency('Bimonthly') == ore.Bimonthly
    assert parseFrequency('Monthly') == ore.Monthly
    assert parseFrequency('EveryFourthWeek') == ore.EveryFourthWeek
    assert parseFrequency('Biweekly') == ore.Biweekly
    assert parseFrequency('Weekly') == ore.Weekly
    assert parseFrequency('Daily') == ore.Daily
    try:
        parseFrequency('unknown')
        assert False
    except Exception as e:
        assert True


def testParseDayCounter():
    assert parseDayCounter('Actual365') == ore.Actual365Fixed()
    assert parseDayCounter('Actual360') == ore.Actual360()
    assert parseDayCounter('Thirty360') == ore.Thirty360(
        ore.Thirty360.BondBasis)
    try:
        parseDayCounter('unknown')
        assert False
    except Exception as e:
        assert True


def testParseCalendar():
    assert parseCalendar('TARGET') == ore.TARGET()
    assert parseCalendar('UnitedStates') == ore.UnitedStates(
        ore.UnitedStates.GovernmentBond)
    assert parseCalendar('Chile') == ore.Chile()
    assert parseCalendar('Brazil') == ore.Brazil()
    assert parseCalendar('NullCalendar') == ore.NullCalendar()
    try:
        parseCalendar('unknown')
        assert False
    except Exception as e:
        assert True


def testParseBusinessDayConvention():
    assert parseBusinessDayConvention('Following') == ore.Following
    assert parseBusinessDayConvention(
        'ModifiedFollowing') == ore.ModifiedFollowing
    assert parseBusinessDayConvention('Preceding') == ore.Preceding
    assert parseBusinessDayConvention(
        'ModifiedPreceding') == ore.ModifiedPreceding
    assert parseBusinessDayConvention('Unadjusted') == ore.Unadjusted
    assert parseBusinessDayConvention(
        'HalfMonthModifiedFollowing') == ore.HalfMonthModifiedFollowing
    try:
        parseBusinessDayConvention('unknown')
        assert False
    except Exception as e:
        assert True


def testParseTimeUnit():
    assert parseTimeUnit('Days') == ore.Days
    assert parseTimeUnit('Weeks') == ore.Weeks
    assert parseTimeUnit('Months') == ore.Months
    assert parseTimeUnit('Years') == ore.Years
    try:
        parseTimeUnit('unknown')
        assert False
    except Exception as e:
        assert True


def testParseDateGenerationRule():
    assert parseDateGenerationRule('Backward') == ore.DateGeneration.Backward
    assert parseDateGenerationRule('Forward') == ore.DateGeneration.Forward
    assert parseDateGenerationRule('Zero') == ore.DateGeneration.Zero
    assert parseDateGenerationRule(
        'ThirdWednesday') == ore.DateGeneration.ThirdWednesday
    assert parseDateGenerationRule('Twentieth') == ore.DateGeneration.Twentieth
    assert parseDateGenerationRule(
        'TwentiethIMM') == ore.DateGeneration.TwentiethIMM
    assert parseDateGenerationRule('OldCDS') == ore.DateGeneration.OldCDS
    assert parseDateGenerationRule('CDS') == ore.DateGeneration.CDS
    assert parseDateGenerationRule('CDS2015') == ore.DateGeneration.CDS2015
    try:
        parseDateGenerationRule('unknown')
        assert False
    except Exception as e:
        assert True


def testParseDate():
    assert parseDate('today') == ore.Date.todaysDate()
    assert parseDate('2019-01-01') == ore.Date(1, 1, 2019)
    try:
        parseDate('unknown')
        assert False
    except Exception as e:
        assert True


def testParsePeriod():
    assert parsePeriod('1D') == ore.Period(1, ore.Days)
    assert parsePeriod('1W') == ore.Period(1, ore.Weeks)
    assert parsePeriod('1M') == ore.Period(1, ore.Months)
    assert parsePeriod('1Y') == ore.Period(1, ore.Years)
    try:
        parsePeriod('unknown')
        assert False
    except Exception as e:
        assert True


def testParseCurrency():
    assert parseCurrency('USD') == ore.USDCurrency()
    assert parseCurrency('EUR') == ore.EURCurrency()
    assert parseCurrency('CLP') == ore.CLPCurrency()
    assert parseCurrency('BRL') == ore.BRLCurrency()
    assert parseCurrency('CLF') == ore.CLFCurrency()
    assert parseCurrency('JPY') == ore.JPYCurrency()
    assert parseCurrency('CHF') == ore.CHFCurrency()
    assert parseCurrency('COP') == ore.COPCurrency()
    assert parseCurrency('MXN') == ore.MXNCurrency()
    assert parseCurrency('PEN') == ore.PENCurrency()
    try:
        parseCurrency('unknown')
        assert False
    except Exception as e:
        assert True


def testParseMonth():
    assert parseMonth('January') == ore.January
    assert parseMonth('February') == ore.February
    assert parseMonth('March') == ore.March
    assert parseMonth('April') == ore.April
    assert parseMonth('May') == ore.May
    assert parseMonth('June') == ore.June
    assert parseMonth('July') == ore.July
    assert parseMonth('August') == ore.August
    assert parseMonth('September') == ore.September
    assert parseMonth('October') == ore.October
    assert parseMonth('November') == ore.November
    assert parseMonth('December') == ore.December
    try:
        parseMonth('unknown')
        assert False
    except Exception as e:
        assert True

# Test case 1
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
assert parse(**kwargs) == expected_result

# Test case 2
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
assert parse(**kwargs) == expected_result

# Test case 3
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
assert parse(**kwargs) == expected_result