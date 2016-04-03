from flask import Flask, request
import json
from utils import coord_distance, _sort_accidents_dist

HEATMAP_RADIUS = 150
HEATMAP_MIN_ACCIDENTS = 100

data = None
with open("random.json", 'r') as f:
    data = json.loads(f.read())

app = Flask(__name__)

@app.route("/heatmap_coords")
def get_coords():
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    if lat is None or lon is None:
        return "Parameters not provided", 403

    lat, lon = map(float, (lat, lon))

    consider_accidents = sorted(data, key=_sort_accidents_dist(lat, lon))

    result = []
    for count, accident in enumerate(consider_accidents):
        dist = coord_distance(lat, lon,
                                accident['location']['latitude'],
                                accident['location']['longitude'])
        if dist > HEATMAP_RADIUS and count > HEATMAP_MIN_ACCIDENTS:
            break

        result.append({
            'l': accident['location']['latitude'],
            'L': accident['location']['longitude'],
            'D': accident['damageRating']
            })

    result_actual = {'accidents': result}
    print "sent ", str(len(result)), "accidents"
    return json.dumps(result_actual)

@app.route("/nearest_accident")
def nearest_accident():
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
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
