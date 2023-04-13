from parsing.parsers import *
from parsing.enums import *
from parsing.others import *
from parsing.ratehelpers import *


class CurveManager:
    def __init__(self, data):
        self.curveHandles = {}
        self.curves = {}
        self.indexes = {}
        self.initilalize(data)

    def getCurve(self, curveName):
        return self.curves[curveName]

    def getIndex(self, indexName):
        return self.indexes[indexName]

    def initialize(self, data):
        refDate = parseDate(data['refDate'])
        ore.Settings.instance().evaluationDate = refDate

        tmpData = {}
        for curve in data['curves']:
            curveName = curve['curveName']
            tmpData[curveName] = curve

        dependencies = getDependencyList(data)
        sortedList = topologicalSort(dependencies)

        for curveName in sortedList:
            parsed = parse(tmpData[curveName])
            self.__buildIndexes(parsed)
            self.__buildCurve(parsed)

    def __buildIndexes(self, data):
        name = data['curveName']
        config = data['curveIndex']
        indexType = IndexType(config['indexType'])

        handle = ore.YieldTermStructureHandle()
        self.curveHandles[name] = handle
        if indexType == IndexType.IborIndex:
            index = createIborIndex(config, handle)
        elif indexType == IndexType.OISIndex:
            index = createOvernightIndex(config, handle)
        self.indexes[name] = index

    def __buildCurve(self, data):
        curveName = data['curveName']
        if data['curveType'] == CurveType.Piecewise:
            curve = self.__buildPiecewiseCurve(data)
        elif data['curveType'] == CurveType.Discount:
            curve = self.__buildDiscountingCurve(data)
        elif data['curveType'] == CurveType.FlatForward:
            curve = self.__buildFlatForwardCurve(data)
        else:
            raise Exception('Unknown curve type: {}'.format(data['curveType']))

        self.curveHandles[curveName].linkTo(curve)
        self.curves[curveName] = curve

    def __buildPiecewiseCurve(self, data):
        rateHelpers = []
        config = data['curveConfig']
        for rateHelper in ['rateHelpers']:
            helperType = HelperType(rateHelper['helperType'])
            helperConfig = rateHelper['helperConfig']
            marketConfig = rateHelper['marketConfig']
            try:
                if helperType == HelperType.Deposit:
                    createDepositRateHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.OIS:
                    createOISRateHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.Swap:
                    createSwapRateHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.TenorBasis:
                    createTenorBasisSwap(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.Xccy:
                    createCrossCcyFixFloatSwapHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.FxSwap:
                    createFxSwapRateHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.SofrFuture:
                    createSofrFutureRateHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.XccyBasis:
                    createCrossCcyBasisSwapHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                elif helperType == HelperType.Bond:
                    createFixedRateBondHelper(
                        helperConfig, marketConfig, self.curves, self.indexes)
                else:
                    raise Exception(
                        'Unknown rate helper type: {}'.format(helperType))
            except Exception as e:
                raise Exception('Failed to create rate helper {helper} at curve {curveName}: {error} '.format(
                    helper=helperType, curveName=data['curveName'], error=e))
            rateHelpers.append(rateHelper)

        refDate = ore.Settings.instance().evaluationDate()
        dayCounter = config['dayCounter']
        curve = ore.PiecewiseYieldCurve(refDate, rateHelpers, dayCounter)
        curve.enableExtrapolation(config['enableExtrapolation'])
        curve.unregisterWithAll()
        return curve

    def __buildDiscountingCurve(self, data):
        raise NotImplementedError("Discounting curve not implemented yet")

    def __buildFlatForwardCurve(self, data):
        raise NotImplementedError("Flat forward curve not implemented yet")
