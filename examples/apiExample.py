from flask import Flask, request
import curveengine as ce

'''
    Codigo de referencia
'''
app = Flask('app')
# post


@app.route('/bootstrap', methods=['POST'])
def bootstrap():
    params = request.get_json()
    try:
        cm = ce.CurveEngine(params)
        bootstrapResults = []
        for curveName, curve in cm.curves.items():
            curveResults = {}
            nodes = [{'date': ce.parseOREDate(tup[0]), 'value': tup[1]}
                     for tup in curve.nodes()]
            curveResults['curveName'] = curveName
            curveResults['curveConfig'] = {
                'curveType': 'Discount',
                'dayCounter': 'Actual360',
                'enableExtrapolation': True,
                'currency': getCurrency(params, curveName),
                'nodes': nodes,
            }
            curveResults['curveIndex'] = getIndex(params, curveName)
            bootstrapResults.append(curveResults)
    except Exception as e:
        return {'statusCode': 400, 'data': formatNestedException(e)}

    results = {
        'curveSetName': params['curveSetName'],
        'refDate': params['refDate'],
        'curves': bootstrapResults
    }

    return {'statusCode': 200, 'data': results}


def getCurrency(config: dict, lookupCurve: str):
    for curve in config['curves']:
        if curve['curveName'] == lookupCurve:
            return curve['curveConfig']['currency']


def getIndex(config: dict, lookupCurve: str):
    for curve in config['curves']:
        if curve['curveName'] == lookupCurve:
            return curve['curveIndex']


def formatNestedException(e: Exception) -> str:
    msg = []
    level = 0
    while e.__cause__ is not None:
        level += 1
        msg.append('Level ' + str(level) + ': ' + str(e))
        e = e.__cause__
    msg.append('Level ' + str(level + 1) + ': ' + str(e))
    return msg


if __name__ == '__main__':
    app.run(debug=True)
