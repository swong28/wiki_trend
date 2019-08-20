#!/usr/bin/env python3

from aws_cdk import core

from wiki_trend_cdk.wiki_trend_cdk_stack import WikiTrendCdkStack


app = core.App()
WikiTrendCdkStack(app, "wiki-trend-cdk-develop", env={'region': 'us-east-1', 'branch': 'develop'})
WikiTrendCdkStack(app, "wiki-trend-cdk-master", env={'region': 'us-east-1', 'branch': 'master'})
app.synth()
