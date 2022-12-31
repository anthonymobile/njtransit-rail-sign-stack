from aws_cdk import (
    CfnOutput,
    Stack,
    aws_lambda as _lambda,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    # aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_alpha as apigwv2,
    aws_apigatewayv2_integrations_alpha as integrations
    aws_lambda_python_alpha as python_alpha
)

from constructs import Construct

import lambda_fns.config as cfg

class NjtsignRailCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # # defines an AWS  Lambda resource
        # # Code loaded from the /lambda_fns dir
        # njtsign_rail_lambda = _lambda.Function(
        #     self, "NJTSignRail_LambdaHandler",
        #     runtime=_lambda.Runtime.PYTHON_3_8,
        #     handler="lambda.handler",
        #     code=_lambda.Code.from_asset("lambda_fns")
        #     )

        # defines an AWS Lambda resource
        # flask app using flask-lambda
        # Code loaded from the /lambda_fns dir
        njtsign_rail_lambda = _lambda.Function(
            self, 
            "NJTSignRail_LambdaHandler",
            handler= "lambda.lambda_handler", #TODO: try lambda.handler
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("./lambda_fns")
        )

PythonFunction(this, 'MyLambda', {
    entry: './lambda/',
    runtime: Runtime.PYTHON_3_8,
    index: 'main.py',
    handler: 'lambda_handler',
    environment: {
        // define env variables if needed
    },
    timeout: Duration.minutes(1)
});




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

        # outputs
        CfnOutput(self, 'HTTP API Url', value=api.url);

