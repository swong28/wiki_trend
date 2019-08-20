from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_iam as iam,
)

import os

class Roles(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        branch = id.split('-')[-1]

        # Lambda 
        self.GitMergeRole = iam.Role(
            self, 'GitMergeRole-'+branch,
            assumed_by= iam.ServicePrincipal('lambda.amazonaws.com'),
            path='/'
        )

        # Add Logs
        self.GitMergeRole.add_to_policy(iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["arn:aws:logs:{}:{}:log-group:/aws/lambda/*".format(
                os.environ['AWS_REGION'], os.environ['AWS_ACCOUNT']
            )]
        ))

        # Add Pipeline Policies
        self.GitMergeRole.add_to_policy(iam.PolicyStatement(
            actions=["codepipeline:GetPipeline", "codepipeline:GetPipelineExecution", 
                     "codepipeline:GetPipelineState", "codepipeline:ListPipelines", "codepipeline:ListPipelineExecutions"],
            resources=["arn:aws:codepipeline:{}:{}:*".format(
                os.environ['AWS_REGION'], os.environ['AWS_ACCOUNT']
            )]
        ))

        # Add CodePipeline Policies
        self.GitMergeRole.add_to_policy(iam.PolicyStatement(
            actions=["codepipeline:GetJobDetails", "codepipeline:PutJobSuccessResult", "codepipeline:PutJobFailureResult"],
            resources=["*"]
        ))

        # Add Policies for S3
        self.GitMergeRole.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=["*"]
        ))

        # Add policies for kms
        self.GitMergeRole.add_to_policy(iam.PolicyStatement(
            actions=["ssm:Describe*", "ssm:Get*", "ssm:List*"],
            resources=["*"] # should update later
        ))

        # Add policies for kms
        self.GitMergeRole.add_to_policy(iam.PolicyStatement(
            actions=["kms:Decrypt*"],
            resources=["*"] # should update later
        ))

        # Create CodeBuild IAM Role
        self.CodeBuildServiceRole = iam.Role(
            self, 'CodeBuildServiceRole-'+branch,
            assumed_by=iam.ServicePrincipal('codebuild.amazonaws.com'),
            path='/',
            # inline_policies=["arn:aws:iam::aws:policy/AdministratorAccess"]
        )

        self.CodeBuildServiceRole.add_to_policy(iam.PolicyStatement(
            actions=['ecr:GetAuthorizationToken', "ecr:InitiateLayerUpload", "ecr:PutImage",
                     "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:GetDownloadUrlForLayer",
                     "ecr:BatchCheckLayerAvailability"],
            resources=['*']
        ))