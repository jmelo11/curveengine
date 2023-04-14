from parsing.parsers import *
from parsing.enums import *
from parsing.others import *
from parsing.ratehelpers import *


class CurveManager:
    def __init__(self, data, curves={}, indexes={}):
        self.curveHandles = {None: ore.RelinkableYieldTermStructureHandle()}
        self.curves = curves
        self.indexes = indexes
        self.initialize(data)

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
            parsed = parse(**tmpData[curveName])
            print(parsed)
            if curveName not in self.indexes.keys():
                self.__buildIndexes(parsed)
            if curveName not in self.curves.keys():
                self.__buildCurve(parsed)

    def __buildIndexes(self, data):
        name = data['curveName']
        config = data['curveIndex']
        indexType = config['indexType']
        handle = ore.RelinkableYieldTermStructureHandle()
        self.curveHandles[name] = handle
        if indexType == IndexType.IborIndex:
            index = createIborIndex(name, config, handle)
        elif indexType == IndexType.OvernightIndex:
            index = createOvernightIndex(name, config, handle)
        else:
            raise Exception(
                'Unknown index type: {}'.format(indexType))
        self.indexes[name] = index

    def __buildCurve(self, data):
        curveName = data['curveName']
        config = data['curveConfig']
        if config['curveType'] == CurveType.Piecewise:
            curve = self.__buildPiecewiseCurve(data)
        elif config['curveType'] == CurveType.Discount:
            curve = self.__buildDiscountingCurve(data)
        elif config['curveType'] == CurveType.FlatForward:
            curve = self.__buildFlatForwardCurve(data)
        else:
            raise Exception(
                'Unknown curve type: {}'.format(config['curveType']))

        self.curveHandles[curveName].linkTo(curve)
        self.indexes[curveName] = self.indexes[curveName].clone(
            self.curveHandles[curveName])
        self.curves[curveName] = curve

    def __buildPiecewiseCurve(self, data):
        rateHelpers = []
        config = data['curveConfig']
        for rateHelper in config['rateHelpers']:
            helperType = rateHelper['helperType']
            helperConfig = rateHelper['helperConfig']
            if 'discountCurve' not in helperConfig.keys():
                helperConfig['discountCurve'] = None
            marketConfig = rateHelper['marketConfig']
            try:
                if helperType == HelperType.Deposit:
                    helper = createDepositRateHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.OIS:
                    helper = createOISRateHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.Swap:
                    helper = createSwapRateHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.TenorBasis:
                    helper = createTenorBasisSwap(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.Xccy:
                    helper = createCrossCcyFixFloatSwapHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.FxSwap:
                    helper = createFxSwapRateHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.SofrFuture:
                    helper = createSofrFutureRateHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.XccyBasis:
                    helper = createCrossCcyBasisSwapHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                elif helperType == HelperType.Bond:
                    helper = createFixedRateBondHelper(
                        helperConfig, marketConfig, self.curveHandles, self.indexes)
                else:
                    raise Exception(
                        'Unknown rate helper type: {}'.format(helperType))
            except KeyError as e:
                raise KeyError('Failed to create rate helper {helper} at curve {curveName}: Key not found: {error} '.format(
                    helper=helperType, curveName=data['curveName'], error=e))
            except Exception as e:
                raise Exception('Failed to create rate helper {helper} at curve {curveName}: {error} '.format(
                    helper=helperType, curveName=data['curveName'], error=e))
            rateHelpers.append(helper)

        refDate = ore.Settings.instance().evaluationDate
        dayCounter = config['dayCounter']

        curve = ore.PiecewiseLogLinearDiscount(
            refDate, rateHelpers, dayCounter)
        if 'enableExtrapolation' in config.keys():
            if config['enableExtrapolation']:
                curve.enableExtrapolation()

        return curve

    def __buildDiscountingCurve(self, data):
        config = data['curveConfig']
        dates = [node['date'] for node in config['nodes']]
        dfs = [node['value'] for node in config['nodes']]
        dayCounter = config['dayCounter']
        if dates[0] != ore.Settings.instance().evaluationDate:
            raise Exception(
                'Failed to create curve {}: first date in discount curve must be the evaluation date'.format(data['curveName']))

        if dfs[0] != 1.0:
            raise Exception(
                'Failed to create curve {}: first discount factor in discount curve must be 1.0'.format(data['curveName']))

        curve = ore.DiscountCurve(dates, dfs, dayCounter)
        if 'enableExtrapolation' in config.keys():
            if config['enableExtrapolation']:
                curve.enableExtrapolation()
        return curve

    def __buildFlatForwardCurve(self, data):
        raise NotImplementedError("Flat forward curve not implemented yet")
