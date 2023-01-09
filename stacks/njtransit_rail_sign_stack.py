from aws_cdk import (
    Stack,
    Duration,
    aws_apigatewayv2_alpha as api_gw,
    aws_apigatewayv2_integrations_alpha as integrations,
    CfnOutput,
    aws_lambda_python_alpha as lambda_alpha_,
    aws_lambda as _lambda
)

from constructs import Construct

class NJTransitRailSignService(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        my_handler = lambda_alpha_.PythonFunction(
            self, 
            "flask_app_function",
            entry="./lambda1",
            index="app.py",
            handler="handler",
            timeout=Duration.seconds(60) ,
            runtime=_lambda.Runtime.PYTHON_3_8
            )

        # defines an API Gateway Http API resource backed by our "efs_lambda" function.
        my_api = api_gw.HttpApi(
            self,
            'NJTRailSign API Lambda',
             default_integration=integrations.HttpLambdaIntegration(
                id="lambda1-lambda-proxy",
                handler=my_handler
                )
                )

        CfnOutput(self, 'HTTP API Url', value=my_api.url);


        '''
        ############### IMPORTED

        # create api and domain mapping
        # per https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigatewayv2_alpha/README.html#custom-domain

        # get the hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=cfg.domain
            )
        
        # create certificate
        certificate = acm.DnsValidatedCertificate(
            self,
            "NJTSignRail_LambdaHandler_Certificate",
            domain_name=f"{cfg.subdomain}.{cfg.domain}",
            hosted_zone=hosted_zone,
            region="us-east-1"
            )
        
        # create API DomainName
        dn = apigwv2.DomainName(
            self, 
            "DN",
            domain_name=f"{cfg.subdomain}.{cfg.domain}",
            certificate=certificate
        )

        # create API gateway
        api = apigwv2.HttpApi(self, "HttpProxyProdApi",
            default_integration=integrations.HttpLambdaIntegration("DefaultIntegration", njtsign_rail_lambda),
            # https://${dn.domainName}/foo goes to prodApi $default stage
            default_domain_mapping=apigwv2.DomainMappingOptions(
                domain_name=dn,
                mapping_key="foo"
            )
        )


        '''