import logging
import json

from flask import Flask, request, render_template, url_for
from flask_bootstrap import Bootstrap4

import serverless_wsgi

from Station import Station
import config as cfg

#### INIT ###############################################################################
# logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# flask
app = Flask(
    __name__,
    static_folder="css", 
    static_url_path="/css")
bootstrap = Bootstrap4(app)

#### FLASK ###############################################################################

# url handler
@app.route('/')
def index():

    logger.debug(f"NJTransitRailSignFunction args: {request.args}" )
    logger.info("Information log message....")

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

#### WRAPPER ###############################################################################
# lambda handler (maps requests via serverless-wsgi)
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

#### MAIN ###############################################################################
# We only need this for local execution.

if __name__ == '__main__':
    app.run()
