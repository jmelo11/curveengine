import sys
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')
from curveengine import CurveEngine
import json


def main():
    with open(parent_dir+'/test.json') as f:
        file = json.load(f)

    cm = CurveEngine(file)
    for date, value in cm.getCurve('SOFR').nodes():
        print(date, value)


if __name__ == '__main__':
    main()
