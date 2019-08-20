from aws_cdk import (
    core,
    aws_s3 as s3,
)

import os

class S3_Bucket(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        branch = id.split('-')[-1]

        bucket = s3.Bucket(
            self, 'ArtifactBucket-'+branch,
            versioned=True,
            bucket_name=os.environ['S3_BUCKET_NAME']+branch
        )

        bucket.add_lifecycle_rule(
            noncurrent_version_expiration=core.Duration.days(30),
            enabled=True
        )

        self.ArtifactBucket = bucket

