from parsers import *
from others import *


def createOISRateHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    tenor = helperConfig['tenor']
    calendar = helperConfig['calendar']
    businessDayConvention = helperConfig['convention']

    settlementDays = helperConfig['settlementDays']
    endOfMonth = helperConfig['endOfMonth']
    paymentLag = helperConfig['paymentLag']
    paymentFrequency = helperConfig['paymentFrequency']
    fwdStart = helperConfig['fwdStart']

    rate = marketConfig['rate']
    spread = marketConfig['spread']
    index = indexes[helperConfig['index']]
    discountCurveHandle = curves[helperConfig['discountCurve']]

    rate = ore.QuoteHandle(ore.SimpleQuote(rate))    
    helper = ore.OISRateHelper(settlementDays, tenor, rate, index, discountCurveHandle, endOfMonth,
                               paymentLag, businessDayConvention, paymentFrequency, calendar, fwdStart, spread)
    return helper


def createDepositRateHelper(helperConfig: dict, marketConfig: dict, *args, **kwargs):
    rate = ore.QuoteHandle(ore.SimpleQuote(marketConfig['rate']))
    tenor = helperConfig['tenor']
    settlementDays = helperConfig['settlementDays']
    calendar = helperConfig['calendar']
    convention = helperConfig['convention']
    endOfMonth = helperConfig['endOfMonth']
    dayCounter = helperConfig['dayCounter']
    helper = ore.DepositRateHelper(rate, tenor, settlementDays, calendar,
                                   convention, endOfMonth, dayCounter)
    return helper


def createFixedRateBondHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
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
    collateralCurve = curves[helperConfig['collateralCurve']]

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
        collateralCurve,
        calendar
    )
    return fxSwapRateHelper


def createSofrFutureRateHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
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
    tenor = helperConfig['tenor']
    shortPayTenor = helperConfig['shortPayTenor']
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
        shortPayTenor,
        discountCurve,
        spreadOnShort,
        True
    )

    return tenorBasisSwapHelper


def createCrossCcyFixFloatSwapHelper(helperConfig: dict, marketConfig: dict, curves: dict, indexes: dict, *args, **kwargs):
    tenor = helperConfig['settlementDays']
    dayCounter = helperConfig['dayCounter']
    settlementDays = helperConfig['tenor']
    endOfMonth = helperConfig['endOfMonth']
    convention = helperConfig['tenor']
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
