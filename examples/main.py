import sys
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')
from curveengine import CurveEngine
import json


def main():
    with open(parent_dir+'/ejemplo.json') as f:
        file = json.load(f)

    cm = CurveEngine(file)
    for curveName, curve in cm.curves.items():
        print(curveName, curve.nodes())


if __name__ == '__main__':
    main()
