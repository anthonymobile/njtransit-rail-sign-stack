import logging
import json

from flask import request, render_template
from flask_lambda import FlaskLambda
from flask_bootstrap import Bootstrap4

from Station import Station
import config as cfg

# flask
app = FlaskLambda(__name__)
bootstrap = Bootstrap4(app)

# logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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

#################################
# We only need this for local development.
#################################

if __name__ == '__main__':
    app.run()



'''
############# OLD EXAMPLE LAMBDA FUNCTION
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