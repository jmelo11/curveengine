import sys
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')
from curveengine import CurveEngine
import json


def main():
    with open(parent_dir+'/config.json') as f:
        file = json.load(f)

    cm = CurveEngine(file)
    for date, value in cm.getCurve('CF_USD_SINTETICO_PASIVO').nodes():
        print(date, value)


if __name__ == '__main__':
    main()
