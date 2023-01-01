#!/usr/bin/env python3
import os, json

import aws_cdk as cdk

# load settings
with open('secrets.json') as f:
    secrets = json.load(f)
env = {
    'account': secrets['account'],
    'region': secrets['region']
    }


from stacks.njtransit_rail_sign_stack import NJTransitRailSignService

app = cdk.App()
NJTransitRailSignService(
    app,
    "njtransit-rail-sign-stack",
    env=env
    )

app.synth()
