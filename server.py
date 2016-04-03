from flask import Flask, request
import json
from utils import coord_distance

data = None
with open("random.json", 'r') as f:
    data = json.loads(f.read())

app = Flask(__name__)

@app.route("/heatmap_coords")
def get_coords():
    result = []
    for accident in data:
        result.append({
            'l': accident['location']['latitude'],
            'L': accident['location']['longitude'],
            'D': accident['damageRating']
            })
    return json.dumps(result)

@app.route("/nearest_accident")
def nearest_accident():
    lat = request.args.get('lat', None)
    lon = request.args.get('long', None)
    if lat is None or lon is None:
        return "Parameters not provided", 403

    lat, lon = map(float, (lat, lon))

    nearest_accident = None
    nearest_distance = float("inf")
    for accident in data:
        dist = coord_distance(lat, lon, **accident['location'])
        if dist < nearest_distance:
            nearest_accident = accident
            nearest_distance = dist
    return json.dumps(nearest_accident)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
