import json
# import sys
# #import top level package
# sys.path.append('..')
from curvemanager import CurveManager

with open('piecewise.json') as f:
    data = json.load(f)

cm = CurveManager(data)

for curveName, curve in cm.curves.items():
    print(curveName, curve.nodes())