#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk import (
    aws_apigatewayv2 as api_gw,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    core
)

import lambda_fns.config as cfg

class TheSimpleWebserviceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create api and domain mapping
        # per https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigatewayv2_alpha/README.html#custom-domain

        # get the hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=f"crowdr.org"
            )
        
        #FIXME: error occurs at certificate construct
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_certificatemanager/DnsValidatedCertificate.html
        # Resource handler returned message: "The runtime parameter of nodejs10.x is no longer supported for creating or updating AWS Lambda functions. We recommend you
        # use the new runtime (nodejs16.x) while creating or updating functions. (Service: Lambda, Status Code: 400, Request ID: 2e405ac3-fa7f-4a6a-85b3-e9d244ab8efb)"

        # create certificate
        certificate = acm.DnsValidatedCertificate(
            self,
            "NJTSignRail_LambdaHandler_Certificate",
            domain_name=f"test.crowdr.org",
            hosted_zone=hosted_zone,
            region="us-east-1"
            )
        
        dn = api_gw.DomainName(
            self, 
            "DN",
            domain_name=f"{cfg.subdomain}.{cfg.domain}",
            certificate=certificate
        )
       