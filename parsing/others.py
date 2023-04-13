from parsers import *
from enums import *
from collections import deque


def createOvernightIndex(indexName: str, settlementDays: int, currency: str, calendar: str, dayCounter: str):
    dayCounter = parseDayCounter(dayCounter)
    currency = parseCurrency(currency)
    calendar = parseCalendar(calendar)
    index = ore.OvernightIndex(
        indexName, settlementDays, currency, calendar, dayCounter)
    return index


def createIborIndex(indexName: str, settlementDays: int, period: str, currency: str, calendar: str, businessDayConvention: str, endOfMonth: bool, dayCounter: str):
    dayCounter = parseDayCounter(dayCounter)
    currency = parseCurrency(currency)
    calendar = parseCalendar(calendar)
    period = parsePeriod(period)
    businessDayConvention = parseBusinessDayConvention(businessDayConvention)
    index = ore.IborIndex(indexName, period, settlementDays, currency,
                          calendar, businessDayConvention, endOfMonth, dayCounter)
    return index





def getDependencyList(data: dict) -> dict:
    # possible curve related keys
    pc = ['discountCurve', 'discountingCurve', 'collateralCurve']
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
