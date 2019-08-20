from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    core,
)

import os

class GitHub(core.Construct):

    def __init__(self, scope: core.Construct, id: str, pipeline: codepipeline.Pipeline, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.sourceOutput = codepipeline.Artifact()

        branch = id.split('-')[-1]
        if branch == 'develop':
            trigger = codepipeline_actions.GitHubTrigger('WEBHOOK')
        else:
            trigger = codepipeline_actions.GitHubTrigger('POLL')
        
        sourceAction = codepipeline_actions.GitHubSourceAction(
            action_name='GitHubSource-'+branch,
            owner=os.environ['GITHUB_OWNER'],
            repo=os.environ['GITHUB_REPO'],
            output=self.sourceOutput,
            branch=branch,
            oauth_token=core.SecretValue(os.environ['GITHUB_TOKEN']),
            trigger= trigger,
            run_order= 1
        )

        pipeline.add_stage(
            stage_name='Source-'+branch,
            actions= [sourceAction]
        )
