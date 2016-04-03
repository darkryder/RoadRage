from math import sin, cos, sqrt, atan2, radians

def coord_distance(lat1, lon1, latitude, longitude):
    # approximate radius of earth in km
    R = 6373.0
    dlon = longitude - lon1
    dlat = latitude - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(latitude) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def _sort_accidents_dist(lat, lon):
    def inner(accident):
        return coord_distance(
            lat, lon,
            accident['location']['latitude'], accident['location']['longitude'])
    return inner
