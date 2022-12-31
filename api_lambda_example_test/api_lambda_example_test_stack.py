from aws_cdk import (
    Stack,
    aws_apigatewayv2_alpha as api_gw,
    aws_apigatewayv2_integrations_alpha as integrations,
    CfnOutput,
    aws_lambda_python_alpha as lambda_alpha_,
    aws_lambda as _lambda

)

from constructs import Construct

class ApiLambdaExampleTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        my_handler = lambda_alpha_.PythonFunction(
            self, 
            "helloworld_function",
            entry="./lambda1",
            index="hello_world.py",
            handler="lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8
            )

        # defines an API Gateway Http API resource backed by our "efs_lambda" function.
        my_api = api_gw.HttpApi(
            self,
            'Test API Lambda',
             default_integration=integrations.HttpLambdaIntegration(
                id="lambda1-lambda-proxy",
                handler=my_handler
                )
                )

        CfnOutput(self, 'HTTP API Url', value=my_api.url);