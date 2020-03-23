#!/usr/bin/env python3
from pathlib import Path
from aws_cdk import core, aws_ecs, aws_ecr_assets


class Covid19Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = aws_ecs.Cluster(
            self, "covid-19-cluster", cluster_name="covid-19"
        )

        image = aws_ecs.ContainerImage.from_registry("knowsuchagency/covid-19")

        task = aws_ecs.FargateTaskDefinition(
            self, "covid-19-api-task", cpu=256, memory_limit_mib=512,
        )

        task.add_container("covid-19-api-container", image=image)

        fargate_service = aws_ecs.FargateService(
            self,
            "covid-19-fargate-service",
            task_definition=task,
            cluster=cluster,
        )


app = core.App()
Covid19Stack(app, "covid-19")

app.synth()
