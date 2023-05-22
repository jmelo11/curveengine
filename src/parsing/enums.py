from enum import Enum


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
    FlatForward = "FlatForward"
    Piecewise = "Piecewise"


class IndexType(Enum):
    '''
    Enum for the type of index
    '''
    OvernightIndex = "OvernightIndex"
    IborIndex = "IborIndex"
