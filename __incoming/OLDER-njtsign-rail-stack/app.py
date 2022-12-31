#!/usr/bin/env python3

import json
from aws_cdk import core

from the_simple_webservice.the_simple_webservice_stack import TheSimpleWebserviceStack

# env settings
with open('secrets.json') as f:
    secrets = json.load(f)

env = {
    'account': secrets['account'],
    'region': secrets['region']
    }

# stack
app = core.App()
TheSimpleWebserviceStack(
    app, 
    "njtsign-rail-stack",
    env=env
    )

# synth
app.synth()
