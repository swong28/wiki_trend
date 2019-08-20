from aws_cdk import (
    core,
    aws_ecr as ecr,
)

import os 

class ECRRepo(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        branch = id.split('-')[-1]
        self.flask = ecr.Repository(
            self, 'repo4frontend-'+branch,
            repository_name='wiki-frontend-'+branch,
        )
