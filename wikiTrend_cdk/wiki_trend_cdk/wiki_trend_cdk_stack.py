from aws_cdk import (
    core,
    aws_codepipeline as codepipeline,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_certificatemanager as cmanager,
    aws_route53 as route53,
)
import os

from s3_bucket import S3_Bucket
from roles import Roles
from pipeline import ServicePipeline
from github import GitHub
from git_codebuild import GitCodeBuild
from ecr_repo import ECRRepo

class WikiTrendCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        branch = kwargs['env']['branch']
        # create s3 bucket for CodeCommit artifacts
        s3_bucket = S3_Bucket(self, 's3-'+branch)

        # Create IAM roles for git merge and CodeBuild
        roles = Roles(
            self, 'roles-'+branch
        )

        # Define New Codepipeline
        pipeline = ServicePipeline(
            self, 'pipeline-'+branch,
            bucket=s3_bucket.ArtifactBucket
        )

        # Create GitHub Account
        github = GitHub(
            self, 'GitHubSource-'+branch,
            pipeline=pipeline.pipeline
        )
        
        # Create ECR Repo
        ecr_repo = ECRRepo(
            self, 'ECRRepo-'+branch,
        )

        # Create CodeBuild
        GitCodeBuild(
            self, 'CodeBuild-'+branch,
            source=github.sourceOutput,
            pipeline=pipeline.pipeline,
            bucket=s3_bucket.ArtifactBucket,
            role=roles.CodeBuildServiceRole,
            frontend=ecr_repo.flask.repository_uri,
        )

        # Create VPC for the ecs
        vpc = ec2.Vpc(
            self, "MyVPC-"+branch,
            max_azs=2,
        )

        # Create ECS cluster
        cluster = ecs.Cluster(
            self, 'EC2-Cluster-'+branch,
            vpc=vpc,
        )

        # Add Auto Scaling Group
        for i in range(3):
            cluster.add_capacity(
                "DefaultAutoScalingGroup-"+str(i)+'-'+branch,
                instance_type=ec2.InstanceType("t2.small"),
                allow_all_outbound=True,
                key_name=os.environ['KEYNAME'],
                # vpc_subnets=vpc.public_subnets
            )
        
        if branch == 'master':
            # Add HostedZone
            hosted_zone = route53.HostedZone(
                self, 'hosted-zone-'+branch, 
                # hosted_zone_id='Z3HNUDRBTJMWFV',
                zone_name='wiki-trend.com'
                )
            domain_name = 'wiki-trend.com'
        else:
            hosted_zone = None
            domain_name = None

        # Add Load Balancer
        ecs_service = ecs_patterns.LoadBalancedEc2Service(
            self, 'Ec2Service-'+branch,
            cluster=cluster,
            # service_name='Frontend-1-'+branch,
            memory_limit_mib=2048,
            container_port=80,
            environment={
                "PORT" : '80',
                'NEO4J_USER' : os.environ['NEO4J_USER'],
                'NEO4J_PASSWORD' : os.environ['NEO4J_PASSWORD']
            },
            domain_name=domain_name,
            domain_zone=hosted_zone,
            # image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo.flask),
            public_load_balancer=True,
        )

        
        core.CfnOutput(
            self, 'ECRRepoURI-'+branch,
            description="The URI of the ECR Repo for flask frontend",
            value=ecr_repo.flask.repository_uri
        )

        core.CfnOutput(
            self, "CodePipelinURL-"+branch,
            description="The URL of the created Pipeline",
            value="https://{}.console.aws.amazon.com/codepipeline/home?region={}#/view/{}".format(
                os.environ['AWS_REGION'],
                os.environ['AWS_REGION'],
                pipeline.pipeline.pipeline_name
            )
        )

        core.CfnOutput(
            self, "LoadBalancerDNS-"+branch,
            value=ecs_service.load_balancer.load_balancer_dns_name
        )