import ORE as ore
from parsing.enums import *


def checkDictKeys(data: dict, keys: list, level: str = ''):
    """
    Check if all the keys are present in the dictionary.

    Parameters
    ----------
    data : dict
        The dictionary to be checked.
    keys : list
        A list of keys to be checked for presence.
    level : str, optional
        The level where the error occurred (default is '').

    Raises
    ------
    KeyError
        If any key is missing from the dictionary.
    """
    for key in keys:
        try:
            _ = data[key]
        except KeyError:
            raise KeyError(f"Missing key: '{key}' in {level}.")


def parse(level, **kwargs):
    results = {}
    for key, value in kwargs.items():
        level_key = level + '\\' + key
        if key in ['helperConfig', 'curveIndex', 'curveConfig']:
            results[key] = parse(level=level_key, **value)

        elif key == 'nodes':
            try:
                results[key] = [parseNode(v) for v in value]
            except KeyError:
                raise KeyError(
                    f"Missing key: 'date' or 'rate' in {level_key}.")
            except ValueError:
                raise ValueError(
                    f"Unable to parse item 'date' or 'rate' in {level_key}.")

        elif key == 'marketConfig':
            results[key] = parseMarketConfig(level_key, value)

        elif key in ['curves', 'rateHelpers']:
            results[key] = [parse(level=level_key + '\\{}'.format(i), **v)
                            for i, v in enumerate(value)]

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
            checkDictKeys(kwargs, [key], level=level_key)
            if isinstance(value, str):
                results[key] = value
            else:
                raise ValueError(
                    'unable to parse item {0} with value {1}'.format(key, value))

        elif key in ['couponRate']:
            checkDictKeys(kwargs, [key], level=level_key)
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


def parseMarketConfig(level, marketConfig):
    results = {}
    if isinstance(marketConfig, dict):
        for key, value in marketConfig.items():
            if key in ['spread', 'fxSpot', 'fxPoints', 'price']:
                if isinstance(value, float):
                    results[key] = value
                elif isinstance(value, dict):
                    checkDictKeys(value, ['value'], level=level)
                    results[key] = value['value']
                else:
                    raise ValueError(
                        'unable to parse item in market config {0} with value {1}'.format(key, value))
            elif key == 'rate':
                if isinstance(value, float):
                    results[key] = value
                elif isinstance(value, dict):
                    checkDictKeys(value, ['value'], level=level)
                    results[key] = value['value']
                else:
                    raise ValueError(
                        'unable to parse item in market config {0} with value {1}'.format(key, value))

    else:
        raise NotImplementedError(
            'unknown market config type: {0}'.format(type(marketConfig)))
    return results


def parseOREDate(date: ore.Date) -> str:
    """
    Parse an ORE date to a string

    Parameters
    ----------
    date : ore.Date
        The ORE date

    Returns
    -------
    str
        The string representation of the date
    """
    return '{0}-{1}-{2}'.format(date.year(), date.month(), date.dayOfMonth())


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
    """
    Parse a compounding string to an ORE compounding enum

    Parameters
    ----------
    compounding : str
        The compounding string

    Returns
    -------
    ore.Compounding
        The ORE compounding enum
    """
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
    """
    Parse a frequency string to an ORE frequency enum

    Parameters
    ----------
    frequency : str
        The frequency string

    Returns
    -------
    ore.Frequency
        The ORE frequency enum
    """

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
    """
    Parse a day counter string to an ORE day counter enum

    Parameters
    ----------
    dayCounter : str
        The day counter string

    Returns
    -------
    ore.DayCounter
        The ORE day counter enum
    """
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
    """
    Parse a calendar string to an ORE calendar enum

    Parameters
    ----------
    calendar : str
        The calendar string

    Returns
    -------
    ore.Calendar
        The ORE calendar enum
    """
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
    """
    Parse a business day convention string to an ORE business day convention enum

    Parameters
    ----------
    businessDayConvention : str
        The business day convention string

    Returns
    -------
    ore.BusinessDayConvention
        The ORE business day convention enum
    """

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
    """
    Parse a time unit string to an ORE time unit enum

    Parameters
    ----------
    timeUnit : str
        The time unit string

    Returns
    -------
    ore.TimeUnit
        The ORE time unit enum
    """
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
    """
    Parse a date generation rule string to an ORE date generation rule enum

    Parameters
    ----------
    dateGenerationRule : str
        The date generation rule string

    Returns
    -------
    ore.DateGeneration
        The ORE date generation rule enum
    """
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
    """
    Parse a date string to an ORE date

    Parameters
    ----------
    date : str
        The date string

    Returns
    -------
    ore.Date
        The ORE date
    """

    if date == 'today':
        return ore.Date.todaysDate()
    else:
        return ore.DateParser.parseFormatted(date, '%Y-%m-%d')


def parsePeriod(period: str) -> ore.Period:
    """
    Parse a period string to an ORE period

    Parameters
    ----------
    period : str
        The period string

    Returns
    -------
    ore.Period
        The ORE period
    """
    tenor = ore.PeriodParser.parse(period)
    return tenor


def parseCurrency(currency: str) -> ore.Currency:
    """
    Parse a currency string to an ORE currency

    Parameters
    ----------
    currency : str
        The currency string

    Returns
    -------
    ore.Currency
        The ORE currency
    """
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
    """
    Parse a month string to an ORE month enum

    Parameters
    ----------
    month : str
        The month string

    Returns
    -------
    ore.Month
        The ORE month enum
    """
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
