from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam
)

import os 

class GitCodeBuild(core.Construct):

    def __init__(self, scope: core.Construct, id: str, source: codepipeline.Artifact, 
                 pipeline: codepipeline.Pipeline, bucket: s3.Bucket, role: iam.Role, 
                 frontend: str, **kwargs) -> None:
                 
        super().__init__(scope, id, **kwargs)

        branch = id.split('-')[-1]

        # Code build for flask frontend
        env = codebuild.BuildEnvironment(
            build_image=codebuild.LinuxBuildImage.UBUNTU_14_04_DOCKER_18_09_0,
            compute_type=codebuild.ComputeType.SMALL,
            environment_variables=
                {
                    'PROJECTNAME':codebuild.BuildEnvironmentVariable(value=os.environ['GITHUB_REPO']),
                    'GITHUBUSER': codebuild.BuildEnvironmentVariable(value=os.environ['GITHUB_OWNER']),
                    'SOURCEBRANCH': codebuild.BuildEnvironmentVariable(value=branch),
                    'ARTIFACT_BUCKET': codebuild.BuildEnvironmentVariable(value=bucket.bucket_arn),
                    'REPO_URI' : codebuild.BuildEnvironmentVariable(value=frontend),
                },
            privileged=True,
            )

        project = codebuild.PipelineProject(
            self, 'Build_Frontend-'+branch,
            description='Submit build jobs for {} as part of CI/CD pipeline'.format(
                os.environ['GITHUB_REPO']
            ),
            environment=env,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            role=role
        )

        cb_actions = codepipeline_actions.CodeBuildAction(
            action_name='CodeBuild-'+branch,
            input=source,
            project=project,
            run_order=3
        )

        pipeline.add_stage(
            stage_name='CodeBuild-'+branch,
            actions=[cb_actions]
        )