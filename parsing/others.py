from parsing.parsers import *
from parsing.enums import *
from collections import deque


def createOvernightIndex(name: str, indexConfig: dict, handle: ore.YieldTermStructureHandle):
    dayCounter = indexConfig['dayCounter']
    currency = indexConfig['currency']
    calendar = indexConfig['calendar']
    fixingDays = indexConfig['fixingDays']
    index = ore.OvernightIndex(
        name, fixingDays, currency, calendar, dayCounter)
    return index


def createIborIndex(name: str, indexConfig: dict, handle: ore.YieldTermStructureHandle):
    dayCounter = indexConfig['dayCounter']
    currency = indexConfig['currency']
    calendar = indexConfig['calendar']
    fixingDays = indexConfig['fixingDays']
    tenor = indexConfig['tenor']
    endOfMonth = indexConfig['endOfMonth']
    convention = indexConfig['convention']
    index = ore.IborIndex(name, tenor, fixingDays, currency,
                          calendar, convention, endOfMonth, dayCounter)
    return index


def getDependencyList(data: dict) -> dict:
    # possible curve related keys
    pc = ['discountCurve', 'collateralCurve']
    # possible index related keys
    pi = ['index', 'shortIndex', 'longIndex']

    dependecies = {}
    for curve in data['curves']:
        curveName = curve['curveName']
        if curveName not in dependecies.keys():
            dependecies[curveName] = set()

        curveConfig = curve['curveConfig']
        curveType = CurveType(curveConfig['curveType'])
        if curveType == CurveType.Piecewise:
            for rateHelper in curveConfig['rateHelpers']:
                config = rateHelper['helperConfig']
                for key in pc:
                    if key in config.keys():
                        dependecies[curveName].add(config[key])
                for key in pi:
                    if key in config.keys():
                        dependecies[curveName].add(config[key])
    return dependecies


def topologicalSort(dependencies):

    for element, deps in dependencies.items():
        deps.discard(element)

    # Find elements with no dependencies
    noDependency = deque([k for k, v in dependencies.items() if not v])

    sortedElements = []

    while noDependency:
        currentElement = noDependency.popleft()
        sortedElements.append(currentElement)

        # Remove the current element as a dependency from other elements
        for element, deps in dependencies.items():
            if currentElement in deps:
                deps.remove(currentElement)
                # If the element now has no dependencies, add it to the queue
                if not deps and element not in noDependency:
                    noDependency.append(element)

    return sortedElements
