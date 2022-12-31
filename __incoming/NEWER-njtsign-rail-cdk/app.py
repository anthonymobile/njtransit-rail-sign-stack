#!/usr/bin/env python3
import os, json

import aws_cdk as cdk

from njtsign_rail_cdk.njtsign_rail_cdk_stack import NjtsignRailCdkStack

# load settings
with open('secrets.json') as f:
    secrets = json.load(f)
env = {
    'account': secrets['account'],
    'region': secrets['region']
    }

# stack
app = cdk.App()
NjtsignRailCdkStack(
    app, 
    "NjtsignRailCdkStack",
    env=env
    )

app.synth()
