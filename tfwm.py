import requests
import os
from dotenv import load_dotenv
import yaml

load_dotenv()

MM_LINE_ID = "4056"

PARAMS = {
    'app_key': os.getenv('app_key'),
    'app_id': os.getenv('app_id'),
    'formatter': 'json'
}

# def get_stops():
#     URL = f"http://api.tfwm.org.uk/Line/{MM_LINE_ID}/StopPoints?"
#     resp = requests.get(URL, params=PARAMS)
#     return resp.json()

# # raw_metro_stops = get_stops()

# # with open('metro_stops.json', 'w') as f:
# #     f.write(json.dumps(raw_metro_stops))

# with open('metro_stops.json', 'r') as f:
#     raw_metro_stops = json.load(f)

# metro_stops = []

# for stop in raw_metro_stops['ArrayOfStopPoint']['StopPoint']:
#     metro_stops.append(stop)

# # Dump metro_stops array into YAML file
# with open('metro_stops.yaml', 'w') as f:
#     yaml.dump(metro_stops, f)

# with open('metro_stops.yaml', 'r') as f:
#     metro_stops = yaml.load(f, Loader=yaml.FullLoader)

def getArrivals():
    URL = f"http://api.tfwm.org.uk/Line/{MM_LINE_ID}/Arrivals?"
    resp = requests.get(URL, params=PARAMS)
    return resp.json()

raw_metro_arrivals = getArrivals()
print(raw_metro_arrivals)

metro_arrivals = []

for arrival in raw_metro_arrivals['ArrayOfPrediction']['Prediction']:
    metro_arrivals.append(arrival)

with open('metro_arrivals.yaml', 'w') as f:
    yaml.dump(metro_arrivals, f)

