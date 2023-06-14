from .parsers import *
from .enums import *
from collections import deque


def createOvernightIndex(name: str, indexConfig: dict, handle: ore.YieldTermStructureHandle):
    """
    Create an overnight index

    Parameters
    ----------
    name : str
        Name of the index
    indexConfig : dict
        Dictionary containing the index configuration
    handle : ore.YieldTermStructureHandle
        Handle to the yield term structure

    Returns
    -------
    ore.OvernightIndex
        Overnight index
    """
    dayCounter = indexConfig['dayCounter']
    currency = indexConfig['currency']
    calendar = indexConfig['calendar']
    fixingDays = indexConfig['fixingDays']
    index = ore.OvernightIndex(
        name, fixingDays, currency, calendar, dayCounter)
    return index


def createIborIndex(name: str, indexConfig: dict, handle: ore.YieldTermStructureHandle):
    """
    Create an ibor index

    Parameters
    ----------
    name : str
        Name of the index
    indexConfig : dict
        Dictionary containing the index configuration
    handle : ore.YieldTermStructureHandle
        Handle to the yield term structure

    Returns
    -------
    ore.IborIndex
        Ibor index
    """
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
    """
    Get the dependency list for the curves.

    Parameters
    ----------
    data : dict
        Dictionary containing the curve data.

    Returns
    -------
    dict
        Dictionary containing the dependency list.

    Notes
    -----
    The dependency list is a dictionary with the curve name as key and a set of
    curve names as value. The set contains the names of the curves that the
    curve depends on.
    """
    # Possible curve-related keys
    pc = ['discountCurve', 'collateralCurve', 'flatDiscountCurve', 'spreadDiscountCurve']
    # Possible index related keys
    pi = ['index', 'shortIndex', 'longIndex', 'flatIndex', 'spreadIndex']

    dependencies = {}
    for curve in data['curves']:
        curveName = curve['curveName']
        if curveName not in dependencies.keys():
            dependencies[curveName] = set()

        curveConfig = curve['curveConfig']
        curveType = CurveType(curveConfig['curveType'])
        if curveType == CurveType.Piecewise:
            for rateHelper in curveConfig['rateHelpers']:
                helperConfig = rateHelper['helperConfig']
                for key in pc:
                    if key in helperConfig:
                        dependencies[curveName].add(helperConfig[key])
                    for key in pi:
                        if key in helperConfig:
                            dependencies[curveName].add(helperConfig[key])
    return dependencies


def topologicalSort(dependencies):
    """
    Sort the dependency list topologically

    Parameters
    ----------
    dependencies : dict
        Dictionary containing the dependency list

    Returns
    -------
    list
        List of curve names sorted topologically
    """
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
