#!/usr/bin/env python3

from aws_cdk import core

from python_lambda_iac_deployment.deployment.cdkworkshop_stack import CdkworkshopStack


app = core.App()
CdkworkshopStack(
    app, "python-lambda-iac-deployment", env={"region": "eu-central-1", "account": "077590795309"}
)

app.synth()
