import aws_cdk as core
import aws_cdk.assertions as assertions

from api_lambda_example_test.api_lambda_example_test_stack import ApiLambdaExampleTestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in api_lambda_example_test/api_lambda_example_test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApiLambdaExampleTestStack(app, "api-lambda-example-test")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
