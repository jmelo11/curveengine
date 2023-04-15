import json
from curvemanager import CurveManager


def main():
    with open('piecewise.json') as f:
        file = json.load(f)

    cm = CurveManager(file)

    for curveName, curve in cm.curves.items():
        print(curveName, curve.nodes())


if __name__ == '__main__':
    main()