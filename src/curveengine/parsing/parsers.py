import ORE as ore
from .enums import *


def parse(**kwargs):
    results = {}
    for key, value in kwargs.items():
        if key in ['helperConfig', 'curveIndex', 'curveConfig']:
            results[key] = parse(**value)

        elif key == 'nodes':
            results[key] = [parseNode(v) for v in value]

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

        elif key in ['settlementDays', 'paymentLag', 'fixingDays']:
            results[key] = int(value)

        elif key == 'month':
            results[key] = parseMonth(value)

        else:
            results[key] = value

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
    day = date.dayOfMonth()
    if day < 10:
        day = '0' + str(date.dayOfMonth())

    month = date.month()
    if date.month() < 10:

        month = '0' + str(date.month())
    return '{0}-{1}-{2}'.format(date.year(), month, day)


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
    try:
        value = Compounding[compounding]
    except KeyError:
        raise NotImplementedError(
            'unknown compounding: {0}'.format(compounding))
    return value.value


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

    try:
        value = Frequency[frequency]
    except KeyError:
        raise NotImplementedError('unknown frequency: {0}'.format(frequency))
    return value.value


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
    try:
        value = DayCounter[dayCounter]
    except KeyError:
        raise NotImplementedError(
            'unknown day counter: {0}'.format(dayCounter))
    return value.value


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
    try:
        value = Calendar[calendar]
    except KeyError:
        raise NotImplementedError('unknown calendar: {0}'.format(calendar))
    return value.value


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

    try:
        value = Convention[businessDayConvention]
    except KeyError:
        raise NotImplementedError(
            'unknown business day convention: {0}'.format(businessDayConvention))
    return value.value


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
    try:
        value = TimeUnit[timeUnit]
    except KeyError:
        raise NotImplementedError('unknown time unit: {0}'.format(timeUnit))
    return value.value


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
    try:
        value = DateGenerationRule[dateGenerationRule]
    except KeyError:
        raise NotImplementedError(
            'unknown date generation rule: {0}'.format(dateGenerationRule))
    return value.value


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
        return ore.DateParser.parseISO(date[0:10])


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
    try:
        value = Currency[currency]
    except KeyError:
        raise NotImplementedError('unknown currency: {0}'.format(currency))
    return value.value


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
    try:
        value = Month[month]
    except KeyError:
        raise NotImplementedError('unknown month: {0}'.format(month))
    return value.value
