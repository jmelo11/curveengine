from parsing.parsers import *
from parsing.others import *


def createOISRateHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create an OIS rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - tenor : str
            The tenor of the helper
        - calendar : str
            The calendar
        - convention : str
            The business day convention
        - settlementDays : int
            The number of settlement days
        - endOfMonth : bool
            Whether the end of month rule is applied
        - paymentLag : int
            The payment lag
        - fixedLegFrequency : str
            The frequency of the fixed leg
        - fwdStart : str
            The forward start
        - index : str
            The index
    marketConfig : dict
        The market configuration for the helper
        - rate : float
            The rate

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.OISRateHelper
        The rate helper
    """
    tenor = helperConfig['tenor']
    calendar = helperConfig['calendar']
    businessDayConvention = helperConfig['convention']

    settlementDays = helperConfig['settlementDays']
    endOfMonth = helperConfig['endOfMonth']
    paymentLag = helperConfig['paymentLag']
    fixedLegFrequency = helperConfig['fixedLegFrequency']
    fwdStart = helperConfig['fwdStart']
    index = indexes[helperConfig['index']]

    rate = marketConfig['rate']
    discountCurve = curves[helperConfig['discountCurve']]

    rate = ore.QuoteHandle(ore.SimpleQuote(rate))
    helper = ore.OISRateHelper(settlementDays, tenor, rate, index, discountCurve, endOfMonth,
                               paymentLag, businessDayConvention, fixedLegFrequency, calendar, fwdStart)
    return helper


def createDepositRateHelper(helperConfig: dict, marketConfig: dict, *args, **kwargs):
    """
    Create a deposit rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - tenor : str
            The tenor of the helper
        - calendar : str
            The calendar
        - convention : str
            The business day convention
        - settlementDays : int
            The number of settlement days
        - endOfMonth : bool
            Whether the end of month rule is applied
        - dayCounter : str
            The day counter
    marketConfig : dict
        The market configuration for the helper
        - rate : float
            The rate

    Returns
    -------
    ore.DepositRateHelper
        The rate helper
    """
    tenor = helperConfig['tenor']
    settlementDays = helperConfig['settlementDays']
    calendar = helperConfig['calendar']
    convention = helperConfig['convention']
    endOfMonth = helperConfig['endOfMonth']
    dayCounter = helperConfig['dayCounter']

    rate = ore.QuoteHandle(ore.SimpleQuote(marketConfig['rate']))
    helper = ore.DepositRateHelper(rate, tenor, settlementDays, calendar,
                                   convention, endOfMonth, dayCounter)
    return helper


def createFixedRateBondHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a fixed rate bond helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - calendar : str
            The calendar
        - convention : str
            The business day convention
        - settlementDays : int
            The number of settlement days
        - couponDayCounter : str
            The day counter for the coupon
        - frequency : str
            The frequency of the coupon
        - tenor: str
            The tenor of the helper
            Optional, if not provided, startDate and endDate must be provided
        - startDate : str
            The start date of the helper
        - endDate : str
            The end date of the helper
    marketConfig : dict
        The market configuration for the helper
        - couponRate : float
            The coupon rate
        - rate : float or ore.InterestRate
            The rate

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.BondHelper
        The rate helper
    """
    calendar = helperConfig['calendar']
    businessDayConvention = helperConfig['convention']
    settlementDays = helperConfig['settlementDays']
    couponDayCounter = helperConfig['couponDayCounter']
    couponRate = marketConfig['couponRate']
    frequency = helperConfig['frequency']

    if 'tenor' in helperConfig.keys():
        tenor = helperConfig['tenor']
        startDate = ore.Settings.instance().evaluationDate()
        maturityDate = startDate + ore.Period(tenor)
    else:
        startDate = helperConfig['startDate']
        maturityDate = helperConfig['endDate']

    # Create a schedule
    schedule = ore.Schedule(
        startDate,
        maturityDate,
        ore.Period(frequency),
        calendar,
        businessDayConvention,
        businessDayConvention,
        ore.DateGeneration.Backward,
        False
    )

    rate = marketConfig['rate']
    if isinstance(rate, float):
        rateDayCounter = ore.Actual365Fixed()
        rateCompounding = ore.Compounded
        rateFrequency = ore.Annual
    elif isinstance(rate, ore.InterestRate):
        rateDayCounter = rate.dayCounter()
        rateCompounding = rate.compounding()
        rateFrequency = rate.frequency()
    else:
        raise Exception('rate is not a float or an InterestRate')

    # Create a fixed rate bond
    fixedRateBond = ore.FixedRateBond(
        settlementDays,
        100,
        schedule,
        [couponRate],
        couponDayCounter,
    )

    # Calculate the clean price
    cleanPrice = fixedRateBond.cleanPrice(
        rate,
        rateDayCounter,
        rateCompounding,
        rateFrequency)

    # Bond helper
    bondHelper = ore.BondHelper(
        ore.QuoteHandle(ore.SimpleQuote(cleanPrice)),
        fixedRateBond
    )

    return bondHelper


def createSwapRateHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - tenor : str
            The tenor of the helper
        - calendar : str
            The calendar
        - convention : str
            The business day convention
        - fixedLegFrequency : str
            The frequency of the fixed leg
        - dayCounter : str
            The day counter
        - index : str
            The index
        - discountCurve : str
            The discounting curve
        - fwdStart : int
            The number of days for the forward start
    marketConfig : dict
        The market configuration for the helper
        - rate : float
            The rate
        - spread : float
            The spread

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.SwapRateHelper
        The rate helper
    """
    tenor = helperConfig['tenor']
    calendar = helperConfig['calendar']
    convention = helperConfig['convention']
    fixedLegFrequency = helperConfig['fixedLegFrequency']
    dayCounter = helperConfig['dayCounter']
    fwdStart = helperConfig['fwdStart']

    # QuoteHandle
    rate = marketConfig['rate']
    spread = marketConfig['spread']
    rateQuote = ore.QuoteHandle(ore.SimpleQuote(rate))
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # Index
    index = indexes[helperConfig['index']]

    # Discounting curve
    discountCurve = curves[helperConfig['discountCurve']]

    # Swap rate helper
    swapRateHelper = ore.SwapRateHelper(
        rateQuote, tenor, calendar, fixedLegFrequency, convention, dayCounter, index, spreadQuote, fwdStart, discountCurve
    )
    return swapRateHelper


def createFxSwapRateHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a fx swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - fixingDays : int
            The number of fixing days
        - calendar : str
            The calendar
        - convention : str
            The business day convention
        - endOfMonth : bool
            Whether the end of month rule applies
        - baseCurrencyAsCollateral : bool
            Whether the base currency is used as collateral
        - tenor : str
            The tenor of the helper
            Optional, if not provided, endDate must be provided
        - endDate : str
            The end date of the helper
        - discountCurve : str
            The discounting curve

    marketConfig : dict
        The market configuration for the helper
        - fxPoints : float
            The fx points
        - fxSpot : float
            The fx spot

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.FxSwapRateHelper
        The rate helper
    """
    fxPoints = marketConfig['fxPoints']
    spotFx = marketConfig['fxSpot']

    fixingDays = helperConfig['fixingDays']
    calendar = helperConfig['calendar']
    convention = helperConfig['convention']
    endOfMonth = helperConfig['endOfMonth']
    baseCurrencyAsCollateral = helperConfig['baseCurrencyAsCollateral']

    if 'tenor' in helperConfig.keys():
        tenor = helperConfig['tenor']
    else:
        startDate = ore.Settings.instance().evaluationDate
        maturityDate = helperConfig['endDate']
        days = maturityDate - startDate
        tenor = ore.Period(days, ore.Days)

    # QuoteHandle
    fwdPointQuote = ore.QuoteHandle(ore.SimpleQuote(fxPoints))
    spotFxQuote = ore.QuoteHandle(ore.SimpleQuote(spotFx))

    # Discounting curve
    discountCurve = curves[helperConfig['discountCurve']]

    # FxSwapRateHelper
    fxSwapRateHelper = ore.FxSwapRateHelper(
        fwdPointQuote,
        spotFxQuote,
        tenor,
        fixingDays,
        calendar,
        convention,
        endOfMonth,
        baseCurrencyAsCollateral,
        discountCurve,
        calendar
    )
    return fxSwapRateHelper


def createSofrFutureRateHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a sofr future rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - month : int
            The month of the helper
        - year : int
            The year of the helper
        - frequency : str
            The frequency of the helper
    marketConfig : dict
        The market configuration for the helper
        - price : float
            The price
        - convexity : float
            The convexity

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.SofrFutureRateHelper
        The rate helper
    """
    month = helperConfig['month']
    year = helperConfig['year']
    frequency = helperConfig['frequency']
    # QuoteHandle
    price = marketConfig['price']
    convexity = marketConfig['convexity']
    priceQuote = ore.QuoteHandle(ore.SimpleQuote(price))
    convexityQuote = ore.QuoteHandle(ore.SimpleQuote(convexity))

    # SofrFutureRateHelper
    sofrFutureRateHelper = ore.SofrFutureRateHelper(
        priceQuote,
        month,
        year,
        frequency,
        convexityQuote
    )
    return sofrFutureRateHelper


def createTenorBasisSwap(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a tenor basis swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - tenor : str
            The tenor of the helper
        - spreadOnShort : bool
            Whether the spread is on the short leg
        - longIndex : str
            The long index
        - shortIndex : str
            The short index
        - discountCurve : str
            The discounting curve

    marketConfig : dict
        The market configuration for the helper
        - spread : float
            The spread

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.TenorBasisSwapHelper
        The rate helper
    """
    tenor = helperConfig['tenor']
    spreadOnShort = helperConfig['spreadOnShort']

    # Index
    longIndex = indexes[helperConfig['longIndex']]
    shortIndex = indexes[helperConfig['shortIndex']]

    # QuoteHandle
    spread = marketConfig['spread']
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # Discounting curve
    discountCurve = curves[helperConfig['discountCurve']]

    # TenorBasisSwapHelper
    tenorBasisSwapHelper = ore.TenorBasisSwapHelper(
        spreadQuote,
        tenor,
        longIndex,
        shortIndex,
        ore.Period(),
        discountCurve,
        spreadOnShort,
        True
    )

    return tenorBasisSwapHelper


def createCrossCcyFixFloatSwapHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a cross currency fix float swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - tenor : str
            The tenor of the helper
        - dayCounter : str
            The day counter
        - settlementDays : int
            The number of settlement days
        - endOfMonth : bool
            Whether the end of month rule applies
        - convention : str
            The business day convention
        - fixedLegFrequency : str
            The frequency of the fixed leg
        - fixedLegCurrency : str
            The currency of the fixed leg
        - calendar : str
            The calendar
        - index : str
            The index
        - discountCurve : str
            The discounting curve

    marketConfig : dict
        The market configuration for the helper
        - rate : float
            The rate
        - fxSpot : float
            The fx spot
        - spread : float
            The spread

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.CrossCcyFixFloatSwapHelper
        The rate helper
    """
    tenor = helperConfig['tenor']
    dayCounter = helperConfig['dayCounter']
    settlementDays = helperConfig['settlementDays']
    endOfMonth = helperConfig['endOfMonth']
    convention = helperConfig['convention']
    fixedLegFrequency = helperConfig['fixedLegFrequency']
    fixedLegCurrency = helperConfig['fixedLegCurrency']
    calendar = helperConfig['calendar']

    # QuoteHandle
    rate = marketConfig['rate']
    spotFx = marketConfig['fxSpot']
    spread = marketConfig['spread']

    rateQuote = ore.QuoteHandle(ore.SimpleQuote(rate))
    spotFxQuote = ore.QuoteHandle(ore.SimpleQuote(spotFx))
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # Index
    index = indexes[helperConfig['index']]

    # Discounting curve
    discountCurve = curves[helperConfig['discountCurve']]

    # CrossCcyFixFloatSwapHelper
    crossCcyFixFloatSwapHelper = ore.CrossCcyFixFloatSwapHelper(
        rateQuote,
        spotFxQuote,
        settlementDays,
        calendar,
        convention,
        tenor,
        fixedLegCurrency,
        fixedLegFrequency,
        convention,
        dayCounter,
        index,
        discountCurve,
        spreadQuote,
        endOfMonth
    )
    return crossCcyFixFloatSwapHelper


def createCrossCcyBasisSwapHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    """
    Create a cross currency basis swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper
        - tenor : str
            The tenor of the helper
        - calendar : str
            The calendar
        - settlementDays : int
            The number of settlement days
        - endOfMonth : bool
            Whether the end of month rule applies
        - convention : str
            The business day convention
        - flatIndex : str
            The flat index
        - spreadIndex : str
            The spread index
        - discountCurve : str
            The discounting curve

    marketConfig : dict
        The market configuration for the helper
        - spread : float
            The spread

    curves : dict
        The curves
    indexes : dict
        The indexes

    Returns
    -------
    ore.CrossCcyBasisSwapHelper
        The rate helper
    """
    tenor = helperConfig['tenor']
    calendar = helperConfig['calendar']
    settlementDays = helperConfig['settlementDays']
    endOfMonth = helperConfig['endOfMonth']
    convention = helperConfig['convention']

    # Discout curves
    flatDiscountCurve = curves[helperConfig['discountCurve']]
    spreadDiscountCurve = curves[helperConfig['discountCurve']]

    # Index
    flatIndex = indexes[helperConfig['flatIndex']]
    spreadIndex = indexes[helperConfig['spreadIndex']]

    # QuoteHandle
    spread = marketConfig['spread']
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # CrossCcyBasisSwapHelper
    crossCcyBasisSwapHelper = ore.CrossCcyBasisSwapHelper(
        spreadQuote,
        tenor,
        calendar,
        settlementDays,
        flatIndex,
        spreadIndex,
        flatDiscountCurve,
        spreadDiscountCurve,
        endOfMonth,
        convention
    )
    return crossCcyBasisSwapHelper
