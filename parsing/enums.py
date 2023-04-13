from enum import Enum


class HelperType(Enum):
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
    Discount = "Discount"
    FlatForward = "FlatForward"
    Piecewise = "Piecewise"


class IndexType(Enum):
    OvernightIndex = "OvernightIndex"
    IborIndex = "IborIndex"


def main():
    tmp = "Deposit"
    print(HelperType(tmp))


if __name__ == "__main__":
    main()
