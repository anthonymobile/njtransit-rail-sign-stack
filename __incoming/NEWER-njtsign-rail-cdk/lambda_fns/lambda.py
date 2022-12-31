from flask import request, render_template
from flask_lambda import FlaskLambda
from flask_bootstrap import Bootstrap4
from Station import *
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
