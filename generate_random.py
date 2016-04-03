from random import randint, choice
import datetime
import radar
import json

EPOCH = datetime.datetime.utcfromtimestamp(0)

def _to_epoch(dt):
    return (dt - EPOCH).total_seconds() * 1000.0

def _random_time():
    return radar.random_datetime(
        start = datetime.datetime(year=2013, month=5, day=24),
        stop = datetime.datetime(year=2016, month=3, day=15)
    )


DETAILS = [
    "Car driver tried to take over another car from wrong side at 90kph hitting the truck standing by the side of road. Accident prone area.",
    "Car driver was pulling into the parking lot driveway when a red Dodge Grand Caravan struck the left side of the vehicle.",
    "The other vehicle struck the car in the rear end",
    "While overtaking, the car collided with another vehicle coming from the other side",
]

def _calc_damage(killed, injured):
    total = float(killed + injured)
    return 0.75*(killed/total) + 0.25*(injured/total)

coords = []
data = []
with open("coords.txt", 'r') as f:
    for combined in f.readlines():
        if combined:
            x, y = map(float, combined.split(','))
            coords.append((x, y))

for x, y in coords:
    killed = randint(0, 5)
    injured = randint(1, 8)
    location = {"latitude": x, "longitude": y}
    details = choice(DETAILS)
    damage = _calc_damage(killed, injured)
    when = _to_epoch(_random_time())
    data.append({
        "location": location,
        "damageRating": damage,
        "killed": killed,
        "injured": injured,
        "datetime": when,
        "crashDetail": details
        })

with open("random.json", 'w') as f:
    f.write(json.dumps(data))
    f.write("\n")
