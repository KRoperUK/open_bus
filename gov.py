import requests
import urllib.parse
import os
import xml.etree.ElementTree as ET 
from dotenv import load_dotenv
import xml.dom.minidom
from siri import parse
import yaml
from copy import deepcopy

def loadRSS(FEED_ID): 
  
    # url of rss feed 
    
    params = {
        'api_key': os.getenv('GOV_API_KEY')
    }

    URL = 'https://data.bus-data.dft.gov.uk/api/v1/datafeed/' + str(FEED_ID) + '/?' + urllib.parse.urlencode(params)
  
    # creating HTTP response object from given url 
    resp = requests.get(URL) 
  
    # saving the xml file 
    with open('data.xml', 'wb') as f: 
        f.write(resp.content) 

def refactorXML(xmlfile):
    # Parse the XML file
    tree = xml.dom.minidom.parse(xmlfile)

    # Get the modified XML as a string
    pretty_xml_as_string = tree.toprettyxml()

    # Remove blank lines
    pretty_xml_as_string = "\n".join(line for line in pretty_xml_as_string.split("\n") if line.strip())

    # Write the modified XML back to the file
    with open(xmlfile, 'w') as f:
        f.write(pretty_xml_as_string)

    return pretty_xml_as_string
def getActivities(xmlfile, operator=None):
    parsed = parse(xmlfile).service_delivery.vehicle_monitoring_delivery

    activities = []
    for child in parsed:
        if child.vehicle_activity:
            for activity in child.vehicle_activity:
                activity = deepcopy(activity)
                obj = {
                    "operator": str(activity.monitored_vehicle_journey.operator_ref),
                    "lineRef": str(activity.monitored_vehicle_journey.line_ref),
                    "directionRef": str(activity.monitored_vehicle_journey.direction_ref),
                    "publishedLineName": str(activity.monitored_vehicle_journey.published_line_name[0].value),
                    "operatorRef": str(activity.monitored_vehicle_journey.operator_ref),
                    "originRef": str(activity.monitored_vehicle_journey.origin_ref),
                    "originName": str(activity.monitored_vehicle_journey.origin_name[0].value),
                    "destinationRef": str(activity.monitored_vehicle_journey.destination_ref),
                    "destinationName": str(activity.monitored_vehicle_journey.destination_name[0].value),
                    "vehicleRef": str(activity.monitored_vehicle_journey.vehicle_ref),
                    "monitored": str(activity.monitored_vehicle_journey.monitored),
                    "delay": str(activity.monitored_vehicle_journey.delay),
                    "vehicleLocation": {
                        "longitude": float(activity.monitored_vehicle_journey.vehicle_location.longitude),
                        "latitude": float(activity.monitored_vehicle_journey.vehicle_location.latitude)
                    },
                    "recordedAtTime": str(activity.recorded_at_time)
                }

                if operator:
                    obj['operator'] = operator

                activities.append(obj)
    return activities
def getServiceNumbers(activities):
    serviceNumbers = []
    for activity in activities:
        serviceNumbers.append(activity['lineRef'])
    return serviceNumbers

def getServiceData(activities, serviceNumber):
    activities = deepcopy(activities)
    return list(filter(lambda activity: activity['lineRef'] == serviceNumber, activities))

def getCoordinates(activities):
    coordinates = []
    for activity in activities:
        tup = (
            float(activity['vehicleLocation']['longitude']),
            float(activity['vehicleLocation']['latitude'])
        )
        coordinates.append(tup)
    return coordinates

def saveCoordinates(coordinates):
    yaml_coordinates = {
        "coordinates": {
        }
    }
    for i, coordinate in enumerate(coordinates):
        yaml_coordinates['coordinates'][i] = {
            "longitude": coordinate[0],
            "latitude": coordinate[1]
        }

    with open('coordinates.yaml', 'w') as f:
        yaml.dump(yaml_coordinates, f)

def refineDirection(activities, direction):
    activities = deepcopy(activities)
    return list(filter(lambda activity: activity['directionRef'] == direction, activities))

def processForMap(activities):
    bus_objects = []
    for activity in activities:
        activity = deepcopy(activity)
        bus_object = {}
        bus_object['vehicleLocation'] = activity['vehicleLocation']
        bus_object['lineRef'] = activity['lineRef']
        bus_object['directionRef'] = activity['directionRef']

        print(activity.keys())
        
        try:
            # Retrieve origin name and destination
            bus_object['origin'] = activity['originName']
            bus_object['destination'] = activity['destinationName']
        except Exception as e:
            bus_object['origin'] = None
            bus_object['destination'] = None
        
        bus_objects.append(bus_object)
    return bus_objects

def mapOutput(activities):
    bus_objects = activities
    yaml_data = {
        "bus_objects": bus_objects
    }
    with open('site/_data/bus_objects.yaml', 'w') as f:
        yaml.dump(yaml_data, f)


load_dotenv()

activities = []

# FIRST BUS
loadRSS(7889)
refactorXML('data.xml')
activities += getActivities('data.xml')

# # BANGA
loadRSS(2519)
refactorXML('data.xml')
activities += getActivities('data.xml')

# # NXWM
loadRSS(10609)
refactorXML('data.xml')
activities += getActivities('data.xml')
os.remove('data.xml')

# # NX Coach
# loadRSS(12319)
# refactorXML('data.xml')
# activities += getActivities('data.xml')

# print(getServiceNumbers(activities))

# activities = getServiceData(activities, '95a') + getServiceData(activities, '95')
# toCrookesMoor = getServiceData(activities, '95a') + getServiceData(activities, '95')
mapOutput(activities)
# toCrookesMoor = refineDirection(toCrookesMoor, 'outbound')
# toCrookesMoorCoordinates = getCoordinates(toCrookesMoor)
# saveCoordinates(toCrookesMoorCoordinates)

# mapOutput(processForMap(toCrookesMoor))