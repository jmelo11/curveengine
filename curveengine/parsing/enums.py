from enum import Enum
import ORE as ore


class HelperType(Enum):
    '''
    Enum for the type of helper
    '''
    Bond = "Bond"
    Deposit = "Deposit"
    FxSwap = "FxSwap"
    OIS = "OIS"
    SofrFuture = "SofrFuture"
    Xccy = "Xccy"
    Swap = "Swap"
    TenorBasis = "TenorBasis"
    XccyBasis = "XccyBasis"


class CurveType(Enum):
    '''
    Enum for the type of curve
    '''
    Discount = "Discount"
    Piecewise = "Piecewise"


class IndexType(Enum):
    '''
    Enum for the type of index
    '''
    OvernightIndex = "OvernightIndex"
    IborIndex = "IborIndex"


class Frequency(Enum):
    '''
    Enum for the frequency of the index
    '''
    Annual = ore.Annual
    Semiannual = ore.Semiannual
    Quarterly = ore.Quarterly
    Monthly = ore.Monthly
    Weekly = ore.Weekly
    Daily = ore.Daily
    Once = ore.Once
    Bimonthly = ore.Bimonthly
    OtherFrequency = ore.OtherFrequency
    EveryFourthMonth = ore.EveryFourthMonth
    EveryFourthWeek = ore.EveryFourthWeek
    Biweekly = ore.Biweekly
    NoFrequency = ore.NoFrequency


class DayCounter(Enum):
    '''
    Enum for the day counter of the index
    '''
    Actual360 = ore.Actual360()
    Actual365 = ore.Actual365Fixed()
    Thirty360 = ore.Thirty360(ore.Thirty360.BondBasis)


class Calendar(Enum):
    '''
    Enum for the calendar of the index
    '''
    NullCalendar = ore.NullCalendar()
    TARGET = ore.TARGET()
    UnitedStates = ore.UnitedStates(ore.UnitedStates.NYSE)
    Chile = ore.Chile()
    Brazil = ore.Brazil()


class Convention(Enum):
    '''
    Enum for the convention of the index
    '''
    Following = ore.Following
    ModifiedFollowing = ore.ModifiedFollowing
    Preceding = ore.Preceding
    ModifiedPreceding = ore.ModifiedPreceding
    HalfMonthModifiedFollowing = ore.HalfMonthModifiedFollowing
    Unadjusted = ore.Unadjusted


class Compounding(Enum):
    '''
    Enum for the compounding of the index
    '''
    Simple = ore.Simple
    Compounded = ore.Compounded
    Continuous = ore.Continuous
    SimpleThenCompounded = ore.SimpleThenCompounded


class TimeUnit(Enum):
    '''
    Enum for the time unit of the index
    '''
    Days = ore.Days
    Weeks = ore.Weeks
    Months = ore.Months
    Years = ore.Years


class DateGenerationRule(Enum):
    '''
    Enum for the date generation rule of the index
    '''
    Backward = ore.DateGeneration.Backward
    Forward = ore.DateGeneration.Forward
    Zero = ore.DateGeneration.Zero
    ThirdWednesday = ore.DateGeneration.ThirdWednesday
    Twentieth = ore.DateGeneration.Twentieth
    TwentiethIMM = ore.DateGeneration.TwentiethIMM
    OldCDS = ore.DateGeneration.OldCDS


class Currency(Enum):
    '''
    Enum for currencies    
    '''
    USD = ore.USDCurrency()
    EUR = ore.EURCurrency()
    GBP = ore.GBPCurrency()
    CHF = ore.CHFCurrency()
    JPY = ore.JPYCurrency()
    CLF = ore.CLFCurrency()
    CLP = ore.CLPCurrency()
    COP = ore.COPCurrency()
    BRL = ore.BRLCurrency()
    MXN = ore.MXNCurrency()
    AUD = ore.AUDCurrency()
    NZD = ore.NZDCurrency()
    SEK = ore.SEKCurrency()
    PEN = ore.PENCurrency()


class Month(Enum):
    '''
    Enum for months
    '''
    January = ore.January
    February = ore.February
    March = ore.March
    April = ore.April
    May = ore.May
    June = ore.June
    July = ore.July
    August = ore.August
    September = ore.September
    October = ore.October
    November = ore.November
    December = ore.December
