from aws_cdk import (
    core,
    aws_codepipeline as codepipeline,
    aws_iam as iam,
    aws_s3 as s3,
)

import os 

class ServicePipeline(core.Construct):

    def __init__(self, scope: core.Construct, id: str, bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        branch = id.split('-')[-1]

        self.pipeline = codepipeline.Pipeline(
            self, 'wiki-Pipeline-'+branch,
            pipeline_name='wiki-Pipeline-'+branch,
            artifact_bucket=bucket
        )

        self.pipeline.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject", "s3:GetObjectVersion", "s3:GetBucketVersioning", "s3:PutObject"],
                resources=[
                    "arn:aws:s3:::{}".format(os.environ['S3_BUCKET_NAME']),
                    "arn:aws:s3:::{}/*".format(os.environ['S3_BUCKET_NAME'])
                ]
            )
        )

        self.pipeline.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "cloudformation:CreateStack", "cloudformation:DeleteStack", "cloudformation:DescribeStacks", 
                    "cloudformation:UpdateStack", "cloudformation:CreateChangeSet", "cloudformation:DeleteChangeSet", 
                    "cloudformation:DescribeChangeSet", "cloudformation:ExecuteChangeSet", "cloudformation:SetStackPolicy", 
                    "cloudformation:ValidateTemplate", "iam:PassRole"
                    ],
                resources=['*']
            )
        )

        self.pipeline.add_to_role_policy(
            iam.PolicyStatement(
                actions=["codebuild:BatchGetBuilds", "codebuild:StartBuild"],
                resources=['*']
            )
        )

        self.pipeline.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "lambda:GetPolicy", "lambda:ListEventSourceMappings", "lambda:ListFunctions", "lambda:InvokeFunction", 
                    "lambda:GetEventSourceMapping", "lambda:GetFunction", "lambda:ListAliases", "lambda:GetAlias", "lambda:ListTags", 
                    "lambda:ListVersionsByFunction", "lambda:GetAccountSettings", "lambda:GetFunctionConfiguration"
                    ],
                resources=['*']
            )
        )