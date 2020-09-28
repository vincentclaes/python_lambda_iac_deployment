from aws_cdk import aws_iam as iam, aws_glue as glue, core, aws_s3_deployment, aws_s3
import os
from python_lambda_iac_deployment import ROOT_DIR


class MyDataScienceStack(core.Construct):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        glue_job_role = iam.Role(
            self,
            "Glue-Job-Role",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ],
        )

        job = glue.CfnJob(
            self,
            "glue-test-job",
            role=glue_job_role.role_arn,
            allocated_capacity=1,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl", script_location="s3://my-bucket/glue-scripts/job.scala"
            ),
            glue_version="2.0",
        )
        #
        # file_asset = aws_s3_assets.Asset(self, "glue-asssets", path=os.path.join(ROOT_DIR, "glue"))
        # print(file_asset.bucket)
        bucket_glue = aws_s3.Bucket(self, "BucketGlue")
        # file_asset = aws_s3_assets.Asset(self, "GlueAssets", path="/Users/vincent/Workspace/python_lambda_iac_deployment/python_lambda_iac_deployment/glue/glue_job.py")
        aws_s3_deployment.BucketDeployment(self, "GlueJobDeployment",
                                           sources=[aws_s3_deployment.Source.asset("/Users/vincent/Workspace/python_lambda_iac_deployment/python_lambda_iac_deployment/glue")],
                                           destination_bucket=bucket_glue,
                                           destination_key_prefix="jobs")