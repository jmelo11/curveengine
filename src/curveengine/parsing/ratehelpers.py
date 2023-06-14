from .parsers import *
from .others import *


def createOISRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create an OIS rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.OISRateHelper
        The rate helper

    See Also
    ----------
    checkOISRateHelper
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

    rate = marketConfig['rate']['value']
    discountCurve = curveHandles[helperConfig['discountCurve']]

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
       
    marketConfig : dict
        The market configuration for the helper
       
    Returns
    -------
    ore.DepositRateHelper
        The rate helper

    See Also
    ----------
    checkDepositRateHelper
    """
    tenor = helperConfig['tenor']
    settlementDays = helperConfig['settlementDays']
    calendar = helperConfig['calendar']
    convention = helperConfig['convention']
    endOfMonth = helperConfig['endOfMonth']
    dayCounter = helperConfig['dayCounter']

    rate = ore.QuoteHandle(ore.SimpleQuote(marketConfig['rate']['value']))
    helper = ore.DepositRateHelper(rate, tenor, settlementDays, calendar,
                                   convention, endOfMonth, dayCounter)
    return helper


def createFixedRateBondRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a fixed rate bond helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.BondHelper
        The rate helper

    See Also
    ----------
    checkFixedRateBondRateHelper
    """
    calendar = helperConfig['calendar']
    businessDayConvention = helperConfig['convention']
    settlementDays = helperConfig['settlementDays']
    couponDayCounter = helperConfig['couponDayCounter']
    couponRate = helperConfig['couponRate']
    frequency = helperConfig['frequency']

    if 'tenor' in helperConfig.keys():
        tenor = helperConfig['tenor']
        startDate = ore.Settings.instance().evaluationDate
        maturityDate = startDate + tenor
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

    rate = marketConfig['rate']['value']
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


def createSwapRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper      

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.SwapRateHelper
        The rate helper

    See Also
    ----------
    checkSwapRateHelper
    """
    tenor = helperConfig['tenor']
    calendar = helperConfig['calendar']
    convention = helperConfig['convention']
    fixedLegFrequency = helperConfig['fixedLegFrequency']
    dayCounter = helperConfig['dayCounter']
    fwdStart = helperConfig['fwdStart']

    # QuoteHandle
    rate = marketConfig['rate']['value']
    spread = marketConfig['spread']['value']
    rateQuote = ore.QuoteHandle(ore.SimpleQuote(rate))
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # Index
    index = indexes[helperConfig['index']]

    # Discounting curve
    discountCurve = curveHandles[helperConfig['discountCurve']]

    # Swap rate helper
    swapRateHelper = ore.SwapRateHelper(
        rateQuote, tenor, calendar, fixedLegFrequency, convention, dayCounter, index, spreadQuote, fwdStart, discountCurve
    )
    return swapRateHelper


def createFxSwapRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a fx swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.FxSwapRateHelper
        The rate helper

    See Also
    ----------
    checkFxSwapRateHelper
    """
    fxPoints = marketConfig['fxPoints']['value']
    spotFx = marketConfig['fxSpot']['value']

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
    discountCurve = curveHandles[helperConfig['discountCurve']]

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


def createSofrFutureRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a sofr future rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.SofrFutureRateHelper
        The rate helper

    See Also
    ----------
    TODO: checkSofrFutureRateHelper
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


def createTenorBasisSwapRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a tenor basis swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.TenorBasisSwapHelper
        The rate helper

    See Also
    ----------
    checkTenorBasisRateHelper
    """
    tenor = helperConfig['tenor']
    spreadOnShort = helperConfig['spreadOnShort']

    # Index
    longIndex = indexes[helperConfig['longIndex']]
    shortIndex = indexes[helperConfig['shortIndex']]

    # QuoteHandle
    spread = marketConfig['spread']['value']
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # Discounting curve
    discountCurve = curveHandles[helperConfig['discountCurve']]

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


def createCrossCcyFixFloatSwapRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a cross currency fix float swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper        

    marketConfig : dict
        The market configuration for the helper

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.CrossCcyFixFloatSwapHelper
        The rate helper

    See Also
    ----------
    checkCrossCcyFixFloatSwapRateHelper
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
    rate = marketConfig['rate']['value']
    spotFx = marketConfig['fxSpot']['value']
    spread = marketConfig['spread']['value']

    rateQuote = ore.QuoteHandle(ore.SimpleQuote(rate))
    spotFxQuote = ore.QuoteHandle(ore.SimpleQuote(spotFx))
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    # Index
    index = indexes[helperConfig['index']]

    # Discounting curve
    discountCurve = curveHandles[helperConfig['discountCurve']]

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


def createCrossCcyBasisSwapRateHelper(helperConfig: dict, marketConfig: dict, curveHandles: dict, indexes: dict, *args, **kwargs):
    """
    Create a cross currency basis swap rate helper

    Parameters
    ----------
    helperConfig : dict
        The configuration for the helper

    marketConfig : dict
        The market configuration for the helper
        - spread : float
            The spread

    curveHandles : dict
        The curveHandles
    indexes : dict
        The indexes

    Returns
    -------
    ore.CrossCcyBasisSwapHelper
        The rate helper

    See Also
    ----------
    checkCrossCcyBasisSwapRateHelper
    """
    tenor = helperConfig['tenor']
    calendar = helperConfig['calendar']
    settlementDays = helperConfig['settlementDays']
    endOfMonth = helperConfig['endOfMonth']
    convention = helperConfig['convention']
    flatIsDomestic = helperConfig['flatIsDomestic']

    # Discout curveHandles
    flatDiscountCurve: ore.RelinkableYieldTermStructureHandle = curveHandles[helperConfig['flatDiscountCurve']]   
    spreadDiscountCurve: ore.RelinkableYieldTermStructureHandle = curveHandles[helperConfig['spreadDiscountCurve']]

    # Index
    flatIndex: ore.IborIndex = indexes[helperConfig['flatIndex']]
    spreadIndex = indexes[helperConfig['spreadIndex']]
    
    # QuoteHandle
    spread = marketConfig['spread']['value']
    spreadQuote = ore.QuoteHandle(ore.SimpleQuote(spread))

    fxSpot = marketConfig['fxSpot']['value']
    fxSpotQuote = ore.QuoteHandle(ore.SimpleQuote(fxSpot))

    # CrossCcyBasisSwapHelper
    crossCcyBasisSwapHelper = ore.CrossCcyBasisSwapHelper(
        spreadQuote,
        fxSpotQuote,
        settlementDays,
        calendar,
        tenor,
        convention,
        flatIndex,
        spreadIndex,
        flatDiscountCurve,
        spreadDiscountCurve,
        endOfMonth,
        flatIsDomestic
    )
    return crossCcyBasisSwapHelper
