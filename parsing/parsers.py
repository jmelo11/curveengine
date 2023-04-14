import ORE as ore
from parsing.enums import *


def parse(**kwargs):
    results = {}
    for key, value in kwargs.items():

        if key in ['helperConfig', 'curveIndex', 'curveConfig']:
            results[key] = parse(**value)

        elif key == 'nodes':
            results[key] = [parseNode(v) for v in value]

        elif key == 'marketConfig':
            results[key] = parseMarketConfig(value)

        elif key in ['curves', 'rateHelpers']:
            results[key] = [parse(**v) for v in value]

        elif key in ['date', 'startDate', 'endDate']:
            results[key] = parseDate(value)

        elif key == 'helperType':
            results[key] = HelperType(value)

        elif key == 'curveType':
            results[key] = CurveType(value)

        elif key == 'indexType':
            results[key] = IndexType(value)

        elif key in ['dayCounter', 'couponDayCounter', 'yieldDayCounter']:
            results[key] = parseDayCounter(value)

        elif key == 'compounding':
            results[key] = parseCompounding(value)

        elif key in ['frequency', 'paymentFrequency', 'fixedLegFrequency', 'floatingLegFrequency']:
            results[key] = parseFrequency(value)

        elif key in ['currency', 'fixedLegCurrency']:
            results[key] = parseCurrency(value)

        elif key == 'calendar':
            results[key] = parseCalendar(value)

        elif key == 'convention':
            results[key] = parseBusinessDayConvention(value)

        elif key in ['tenor', 'fwdStart', 'shortPayTenor']:
            results[key] = parsePeriod(value)

        elif key in ['endOfMonth', 'telescopicValueDates', 'spreadOnShortIndex', 'baseCurrencyAsCollateral', 'enableExtrapolation']:
            if isinstance(value, bool):
                results[key] = value
            else:
                raise ValueError(
                    'unable to parse item {0} with value {1}'.format(key, value))

        elif key in ['settlementDays', 'paymentLag', 'fixingDays', 'year']:
            if isinstance(value, int):
                results[key] = value
            else:
                raise ValueError(
                    'unable to parse item {0} with value {1}'.format(key, value))

        elif key in ['discountCurve', 'index', 'shortIndex', 'longIndex', 'curveName']:
            if isinstance(value, str):
                results[key] = value
            else:
                raise ValueError(
                    'unable to parse item {0} with value {1}'.format(key, value))

        elif key in ['couponRate']:
            if isinstance(value, float):
                results[key] = value
            else:
                raise ValueError(
                    'unable to parse item {0} with value {1}'.format(key, value))

        elif key == 'month':
            results[key] = parseMonth(value)

        else:
            results[key] = value

    return results


def parseMarketConfig(marketConfig):
    results = {}
    if isinstance(marketConfig, dict):
        for key, value in marketConfig.items():
            if key in ['spread', 'fxSpot', 'fxPoints', 'price']:
                if isinstance(value, float):
                    results[key] = value
                elif isinstance(value, dict):
                    results[key] = value['value']
                else:
                    raise ValueError(
                        'unable to parse item in market config {0} with value {1}'.format(key, value))
            elif key == 'rate':
                if isinstance(value, float):
                    results[key] = value
                elif isinstance(value, dict):
                    results[key] = value['value']
                else:
                    raise ValueError(
                        'unable to parse item in market config {0} with value {1}'.format(key, value))

    else:
        raise NotImplementedError(
            'unknown market config type: {0}'.format(type(marketConfig)))
    return results


def parseNode(node):
    return {'date': parseDate(node['date']), 'value': node['value']}


def createInterestRate(
        rate: float,
        dayCount: str,
        compounding: str,
        frequency: str) -> ore.InterestRate:
    return ore.InterestRate(
        rate,
        parseDayCounter(dayCount),
        parseCompounding(compounding),
        parseFrequency(frequency))


def parseCompounding(compounding: str):
    if compounding == 'Simple':
        return ore.Simple
    elif compounding == 'Compounded':
        return ore.Compounded
    elif compounding == 'Continuous':
        return ore.Continuous
    else:
        raise NotImplementedError(
            'unknown compounding: {0}'.format(compounding))


def parseFrequency(frequency: str):
    if frequency == 'Once':
        return ore.Once
    elif frequency == 'Annual':
        return ore.Annual
    elif frequency == 'Semiannual':
        return ore.Semiannual
    elif frequency == 'EveryFourthMonth':
        return ore.EveryFourthMonth
    elif frequency == 'Quarterly':
        return ore.Quarterly
    elif frequency == 'Bimonthly':
        return ore.Bimonthly
    elif frequency == 'Monthly':
        return ore.Monthly
    elif frequency == 'EveryFourthWeek':
        return ore.EveryFourthWeek
    elif frequency == 'Biweekly':
        return ore.Biweekly
    elif frequency == 'Weekly':
        return ore.Weekly
    elif frequency == 'Daily':
        return ore.Daily
    else:
        raise NotImplementedError('unknown frequency: {0}'.format(frequency))


def parseDayCounter(dayCounter: ore.DayCounter) -> ore.DayCounter:
    if dayCounter == 'Actual365':
        return ore.Actual365Fixed()
    elif dayCounter == 'Actual360':
        return ore.Actual360()
    elif dayCounter == 'Thirty360':
        return ore.Thirty360(ore.Thirty360.BondBasis)
    else:
        raise NotImplementedError(
            'unknown day counter: {0}'.format(dayCounter))


def parseCalendar(calendar: str) -> ore.Calendar:
    if calendar == 'TARGET':
        return ore.TARGET()
    elif calendar == 'UnitedStates':
        return ore.UnitedStates(ore.UnitedStates.GovernmentBond)
    elif calendar == 'Chile':
        return ore.Chile()
    elif calendar == 'Brazil':
        return ore.Brazil()
    elif calendar == 'NullCalendar':
        return ore.NullCalendar()
    else:
        raise NotImplementedError('unknown calendar: {0}'.format(calendar))


def parseBusinessDayConvention(businessDayConvention: str):
    if businessDayConvention == 'Following':
        return ore.Following
    elif businessDayConvention == 'ModifiedFollowing':
        return ore.ModifiedFollowing
    elif businessDayConvention == 'Preceding':
        return ore.Preceding
    elif businessDayConvention == 'ModifiedPreceding':
        return ore.ModifiedPreceding
    elif businessDayConvention == 'Unadjusted':
        return ore.Unadjusted
    elif businessDayConvention == 'HalfMonthModifiedFollowing':
        return ore.HalfMonthModifiedFollowing
    else:
        raise NotImplementedError(
            'unknown business day convention: {0}'.format(businessDayConvention))


def parseTimeUnit(timeUnit: str):
    if timeUnit == 'Days':
        return ore.Days
    elif timeUnit == 'Weeks':
        return ore.Weeks
    elif timeUnit == 'Months':
        return ore.Months
    elif timeUnit == 'Years':
        return ore.Years
    else:
        raise NotImplementedError('unknown time unit: {0}'.format(timeUnit))


def parseDateGenerationRule(dateGenerationRule: str):
    if dateGenerationRule == 'Backward':
        return ore.DateGeneration.Backward
    elif dateGenerationRule == 'Forward':
        return ore.DateGeneration.Forward
    elif dateGenerationRule == 'Zero':
        return ore.DateGeneration.Zero
    elif dateGenerationRule == 'ThirdWednesday':
        return ore.DateGeneration.ThirdWednesday
    elif dateGenerationRule == 'Twentieth':
        return ore.DateGeneration.Twentieth
    elif dateGenerationRule == 'TwentiethIMM':
        return ore.DateGeneration.TwentiethIMM
    elif dateGenerationRule == 'OldCDS':
        return ore.DateGeneration.OldCDS
    elif dateGenerationRule == 'CDS':
        return ore.DateGeneration.CDS
    elif dateGenerationRule == 'CDS2015':
        return ore.DateGeneration.CDS2015
    else:
        raise NotImplementedError(
            'unknown date generation rule: {0}'.format(dateGenerationRule))


def parseDate(date: str) -> ore.Date:
    if date == 'today':
        return ore.Date.todaysDate()
    else:
        return ore.DateParser.parseFormatted(date, '%Y-%m-%d')


def parsePeriod(period: str) -> ore.Period:
    tenor = ore.PeriodParser.parse(period)
    return tenor


def parseCurrency(currency: str) -> ore.Currency:
    if currency == 'USD':
        return ore.USDCurrency()
    elif currency == 'EUR':
        return ore.EURCurrency()
    elif currency == 'CLP':
        return ore.CLPCurrency()
    elif currency == 'BRL':
        return ore.BRLCurrency()
    elif currency == 'CLF':
        return ore.CLFCurrency()
    elif currency == 'JPY':
        return ore.JPYCurrency()
    elif currency == 'CHF':
        return ore.CHFCurrency()
    elif currency == 'COP':
        return ore.COPCurrency()
    elif currency == 'MXN':
        return ore.MXNCurrency()
    elif currency == 'PEN':
        return ore.PENCurrency()
    else:
        raise NotImplementedError('unknown currency: {0}'.format(currency))


def parseMonth(month: str):
    if month == 'January':
        return ore.January
    elif month == 'February':
        return ore.February
    elif month == 'March':
        return ore.March
    elif month == 'April':
        return ore.April
    elif month == 'May':
        return ore.May
    elif month == 'June':
        return ore.June
    elif month == 'July':
        return ore.July
    elif month == 'August':
        return ore.August
    elif month == 'September':
        return ore.September
    elif month == 'October':
        return ore.October
    elif month == 'November':
        return ore.November
    elif month == 'December':
        return ore.December
    else:
        raise NotImplementedError('unknown month: {0}'.format(month))
