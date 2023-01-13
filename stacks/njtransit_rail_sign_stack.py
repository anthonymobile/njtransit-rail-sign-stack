#TODO: comment out ones that dont need in final

from aws_cdk import (
    Stack,
    Duration,
    aws_apigateway as apigateway,
    CfnOutput,
    aws_lambda_python_alpha as lambda_alpha_,
    aws_lambda as _lambda,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets
)

from constructs import Construct

import lambda1.config as cfg

class NJTransitRailSignService(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        my_handler = lambda_alpha_.PythonFunction(
            self, 
            "NJTRailSign_Lambda",
            entry="./lambda1",
            index="app.py",
            handler="handler",
            timeout=Duration.seconds(60) ,
            runtime=_lambda.Runtime.PYTHON_3_8
            )

        ################################################################################
        # REST API, Custom Domain
        # following https://cloudbytes.dev/aws-academy/cdk-api-gateway-with-custom-domain
        ################################################################################

        # get the hosted zone
        my_hosted_zone = route53.HostedZone.from_lookup(
            self,
            "NJTSignRail_HostedZone",
            domain_name=cfg.domain
            )

        # create certificate
        my_certificate = acm.DnsValidatedCertificate(
            self,
            "NJTSignRail_Certificate",
            domain_name=f"{cfg.subdomain}.{cfg.domain}",
            hosted_zone=my_hosted_zone,
            region="us-east-1"
            )

        # create REST API
        my_api = apigateway.LambdaRestApi(
            self,
            "NJTSignRail_ApiGateway",
            handler=my_handler,
            domain_name=apigateway.DomainNameOptions(
                domain_name=f"{cfg.subdomain}.{cfg.domain}",
                certificate=my_certificate,
                security_policy=apigateway.SecurityPolicy.TLS_1_2,
                endpoint_type=apigateway.EndpointType.EDGE,
            )
        )

        # create A record
        route53.ARecord(
            self,
            "NJTSignRail_ApiRecord",
            record_name=cfg.subdomain,
            zone=my_hosted_zone,
            target=route53.RecordTarget.from_alias(targets.ApiGateway(my_api)),
        )


        ################################################################################
        # OUTPUTS
        ################################################################################

        CfnOutput(self, 'Hosted Zone', value=my_hosted_zone.zone_name);
        CfnOutput(self, 'API Url', value=my_api.url);
