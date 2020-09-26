from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from python_lambda_iac_deployment.deployment.hitcounter import HitCounter
from python_lambda_iac_deployment.deployment.glue_job_construct import (
    MyDataScienceStack,
)
from python_lambda_iac_deployment import lambda_function

lambda_function


class CdkworkshopStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            # code=_lambda.Code.asset(lambda_function.__path__[0]),
            code=_lambda.Code.asset(
                "/Users/vincent/Workspace/python_lambda_iac_deployment/python_lambda_iac_deployment/lambda_function"
            ),
            handler="hello.handler",
        )

        hello_with_counter = HitCounter(
            self,
            "HelloHitCounter",
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=hello_with_counter.handler,
        )

        glue_job = MyDataScienceStack(self, "GlueJob")
