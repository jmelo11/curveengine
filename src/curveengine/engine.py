from .parsing.parsers import *
from .parsing.enums import *
from .parsing.others import *
from .parsing.ratehelpers import *
from .parsing.checks import *


class CurveEngine:
    '''
    Class for building curves and indexes from a JSON configuration file.

    Parameters
    ----------
    data : dict
        The JSON configuration file as a dictionary.
    curves : dict, optional
        A dictionary of curves to be populated by the engine. The default is None.
    indexes : dict, optional
        A dictionary of indexes to be populated by the engine. The default is None.

    Returns
    -------
    None
    '''

    def __init__(self, data, curves=None, indexes=None):
        self.curveHandles = {None: ore.RelinkableYieldTermStructureHandle()}
        self.curves = {} if curves is None else curves
        self.indexes = {} if indexes is None else indexes
        localData = data.copy()
        checkConfiguration(localData)
        self.__initialize(localData)

    '''
    Get a curve by name.

    Parameters
    ----------
    curveName : str
        The name of the curve to get.

    Returns
    -------
    ore.YieldTermStructure
        The curve with the given name.
    '''

    def getCurve(self, curveName):
        return self.curves[curveName]

    '''
    Get an index by name.

    Parameters
    ----------
    indexName : str
        The name of the index to get.

    Returns
    -------
    ore.IborIndex or ore.OvernightIndex
        The index with the given name.
    '''

    def getIndex(self, indexName):
        return self.indexes[indexName]

    def __initialize(self, data):
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
        for i, rateHelper in enumerate(config['rateHelpers']):
            helperType = rateHelper['helperType']
            helperConfig = rateHelper['helperConfig']                        
            marketConfig = rateHelper['marketConfig']
        
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
                helper = createTenorBasisSwapRateHelper(
                    helperConfig, marketConfig, self.curveHandles, self.indexes)
            elif helperType == HelperType.Xccy:
                helper = createCrossCcyFixFloatSwapRateHelper(
                    helperConfig, marketConfig, self.curveHandles, self.indexes)
            elif helperType == HelperType.FxSwap:
                helper = createFxSwapRateHelper(
                    helperConfig, marketConfig, self.curveHandles, self.indexes)
            elif helperType == HelperType.SofrFuture:
                helper = createSofrFutureRateHelper(
                    helperConfig, marketConfig, self.curveHandles, self.indexes)
            elif helperType == HelperType.XccyBasis:
                helper = createCrossCcyBasisSwapRateHelper(
                    helperConfig, marketConfig, self.curveHandles, self.indexes)
            elif helperType == HelperType.Bond:
                helper = createFixedRateBondRateHelper(
                    helperConfig, marketConfig, self.curveHandles, self.indexes)
          
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
