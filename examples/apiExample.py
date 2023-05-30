from flask import Flask, request
import sys
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir + '/../src')
from curveengine import CurveEngine

'''
    Codigo de referencia
'''
app = Flask('app')
# post

@app.route('/bootstrap', methods=['POST'])
def bootstrap():
    params = request.get_json()
    cm = CurveEngine(data=params)
    results = {}
    for curveName, curve in cm.curves.items():
        try:
            curveNodes = [{'date': str(tup[0]), 'value': tup[1]}
                          for tup in curve.nodes()]
            results[curveName] = curveNodes
        except Exception as e:
            raise e
    return results


if __name__ == '__main__':
    app.run()
