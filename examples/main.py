import json
from curveengine import CurveEngine
import sys


def main():    
    with open('piecewise.json') as f:
        file = json.load(f)

    cm = CurveEngine(file)

    for curveName, curve in cm.curves.items():
        print(curveName, curve.nodes())


if __name__ == '__main__':
    main()