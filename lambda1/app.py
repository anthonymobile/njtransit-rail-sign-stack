import json
from util import get_util_string
import requests
import logging

from flask import request, render_template

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    logger.debug(f"NJTransitRailSignFunction Event: {event}")

    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)

        raise e

    # test that we can call a function from another python file
    s = get_util_string()

    logger.info("Goodbye World....")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "NJTransit Sign Is Alive!",
            "location": ip.text.replace("\n", ""),
            "util_string": s
        }),
    }


'''
############# IMPORTED
from flask import request, render_template
from flask_lambda import FlaskLambda
from flask_bootstrap import Bootstrap4
import config as cfg

#################################
# WEB APP
#################################

app = FlaskLambda(__name__)
bootstrap = Bootstrap4(app)

@app.route('/')
def index():

    station_code = request.args.get('station_code')
    if station_code is None:
        return("ERROR: No station code provided.")
    else:
        station = Station(station_code)
        return render_template(
            'index.html',
            cfg=cfg,
            station_name=station.station_name,
            arrivals=station.arrivals
        )


# filter. insert a newline into the headsign.
@app.template_filter()
def headsign(fd):
    headsign = fd.replace(' ','<br/>', 1)
    return headsign

# filter. rewrite the  messages for better display
@app.template_filter()
def message_fix(message):
    if message in cfg.message_replacements:
        return cfg.message_replacements[message]
    else:
        return message.lower()

#################################
# We only need this for local development.
#################################

if __name__ == '__main__':
    app.run()


#################################
# CLASS
#################################


class Station:

    def __init__(self, station_code):
        self.station_code = station_code
        self.station_name = self.get_station_name()
        self.arrivals_json = self.fetch_arrivals()
        self.arrivals = self.parse_arrivals()

    def __repr__(self):
        return f"Station (station_code={self.station_code}, station_name={self.station_name}, updated={self.arrivals_fetch_time}, no_arrivals={len(self.arrivals)})"

    def get_station_name(self):
        
        # lookup in config.py
        try:
            return cfg.station_names[self.station_code]['station_name']
        except KeyError:
            return 'Station name unknown.'
        
        #TODO look up station name from API via getStationListXML endpoint
        
        # sloppy old way
        # for station_code,station_name in cfg.station_names.items():
        #     if self.station_code == station_code:
        #         self.station_name = station_name
        #         return
        # self.station_name = 'Station name unknown.'
        # return

    def get_secrets(self):
        with open('secrets.json') as f:
            data = json.load(f)
            username = data['username']
            password = data['password']
            return (username, password)


    def fetch_arrivals(self):
        username, password = self.get_secrets()

        #this might be case sensitive? http://traindata.njtransit.com:8092/njttraindata.asmx
        arrivals_json_url=f"http://traindata.njtransit.com:8092/NJTTrainData.asmx/getTrainScheduleJSON19Rec?username={username}&password={password}&station={self.station_code}"

        headers = {'Accept': 'application/json'}
        try:
            r = requests.get(arrivals_json_url, headers=headers)
            return r.json()
        except:
            print(f"Error in arrivals request to {arrivals_json_url}")
            return


    def parse_arrivals(self):

        # process self.arrivals_json into list of dicts for the template to unpack
        arrivals=[]

        # dummy data
        arrivals = [
            {"train_no": "3434", "eta" : "7", "destination" : "Hoboken", "occupancy": "LIGHT" },
            {"train_no": "3411", "eta" : "11", "destination" : "Summit", "occupancy": "MEDIUM" },
            {"train_no": "2711", "eta" : "25", "destination" : "New York", "occupancy": "MEDIUM" }
            ]

        # #TODO: update this when we know what the response looks like
        # for key, value in self.arrival_json:
        #     arrival = {
        #         "train_no": 3434,
        #         "eta" : 7,
        #         "destination" : "Hoboken"
        #     }
        #     arrivals.append(arrival)

        return arrivals



# XML processing stuff, avoid using the XML endpoints if possible

from lxml import html
import xml.etree.ElementTree
from operator import itemgetter
import urllib.request, urllib.error, urllib.parse
from collections import defaultdict
import ast


# parse response
arrivals_list = []
try:
e = xml.etree.ElementTree.fromstring(data)
# error or no data
except:
dummy_record = {
            'rd': str(self.route),
            'fd': 'No service',
            'eta': 'No service',
            'eta_int': 99,
            'v': '0000',
            'pt': '',
            'occupancy': 'NO DATA'
            }
arrivals_list.append(dummy_record)
return arrivals_list

# no arrivals
# x = e.findall('noPredictionMessage')
if e.findall('noPredictionMessage'):
dummy_record = {
            'rd': str(self.route),
            'fd': 'No service',
            'eta': 'No service',
            'eta_int': 99,
            'v': '0000',
            'pt': '',
            'occupancy': 'NO DATA'
            }
arrivals_list.append(dummy_record)
return arrivals_list

# some arrivals
for atype in e.findall('pre'):
fields = {}
for field in atype:
    if field.tag not in fields and hasattr(field, 'text'):
        if field.text is None:
            fields[field.tag] = ''
            continue
        fields[field.tag] = field.text.replace("&nbsp", "") 
arrivals_list.append(fields)

# parse needed fields and update arrivals_list in place
for arrival in arrivals_list:

arrival['stop_id'] = self.stop
arrival['stopname'] = self.stop_name
arrival['eta'] = '0'
if arrival['pt']:
    
    # check for delayed bus and preserve order
    # if so, recode then skip rest of loop
    if arrival['pt'] == "DELAYED":
        
        #FIXME: this needs to be called after the entire arrival list is generated, but before regroup
        #because we sort this later in regroup_arrivals(), need to give DELAYED buses an "estimated" ETA to sequence them properly
        arrival['eta_int'] = self.estimate_delayed_eta(arrivals_list)
        continue
        
    # check for other special messages
    # if so, recode then skip rest of loop
    if arrival['pt'] in cfg.pt_messages:
        arrival['eta_int'] = cfg.pt_messages[arrival['pt']]
        continue
    
    # otherwise split and try to cast as int
    try:
        arrival['eta_int'] = int(arrival['pt'].split(' ')[0])
    
    # unless its a new special message
    except:
        #suppress it
        arrival['eta_int'] = -1
        
        # print to console
        print(f"***********UNEXPECTED 'pt' --> {arrival['pt']} **********")

return arrivals_list[:cfg.num_arrivals_per_route]


#################################
# ARRIVAL DATA FETCH + FORMAT
#################################

def regroup_arrivals(arrivals):
    arrivals_board = []
    for stop, arrival_data in arrivals.items():
        for route, arrivals_list in arrival_data.items():      
            for arrival in arrivals_list:
                arrivals_board.append(arrival)
    for arrival in arrivals_board:
        arrival['fd']=headsign_lookup(arrival['fd'])
    # sort by destination and ETA
    arrivals_board = sorted(arrivals_board, key=itemgetter('fd', 'rd', 'eta_int'))
    return arrivals_board

def headsign_lookup(fd):
    try:
        # split off the route number
        fd = fd.split(" ", 1)[1]
        fd=cfg.headsign_replacements[fd]
        return fd
    except KeyError:
        return fd

def pare_arrivals(arrivals):
    # drop ones under cutoff
    for stop, arrival_data in arrivals.items():
        for route, arrivals_list in arrival_data.items():
            for i,arrival in enumerate(arrivals_list):
                if int(arrival['eta_int']) > cfg.cutoff:
                    del arrivals_list[i]
    return arrivals
'''