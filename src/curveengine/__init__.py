'''
    The CurveEngine package is intended to be used to build curves and indexes from a JSON configuration file, using as backend QuantLib and QuantExt.
    The main class is CurveEngine and has two methods: getCurve and getIndex. The first one returns a curve by name, 
    the second one returns an index by name. 
    
    The class is initialized by the __initialize method, which is called by the constructor. 
    The __initialize method is the one that actually builds the curves and indexes. 
    
    The constructor also takes two optional parameters: curves and indexes. These are dictionaries that can be used to populate the
    curves and indexes of the engine. This is useful when the engine is used to build multiple
    curves and indexes from other builds.
'''

from .engine import *