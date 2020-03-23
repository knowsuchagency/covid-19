import json
import os

import toml
from invoke import task


@task(aliases=["format"])
def black(c):
    c.run("black tasks.py covid_19/ tests/")


@task
def test(c):
    c.run("pytest tests/")


@task
def install_hooks(c):
    """Install git hooks."""
    c.run("pre-commit install")
    c.run("pre-commit install -t pre-push")


@task(aliases=["check-black"])
def check_formatting(c):
    """Check that files conform to black standards."""
    c.run("black --check covid_19/ tests/ tasks.py")


@task(check_formatting, test)
def publish(c, username=None, password=None):
    """Publish to pypi."""

    username = username or os.getenv("PYPI_USERNAME")

    password = password or os.getenv("PYPI_PASSWORD")

    *_, latest_release = json.loads(
        c.run("qypi releases covid-19", hide=True).stdout
    )["covid-19"]

    latest_release_version = latest_release["version"]

    local_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    if local_version == latest_release_version:
        print("local and release version are identical -- skipping publish")
    else:
        print(f"publishing covid-19 v{local_version}")
        c.run(
            f"poetry publish -u {username} -p '{password}' --build",
            pty=True,
            hide=True,
        )


@task
def docker_login(c, username=None, password=None):
    if username is not None:
        username_flag = f"-u {username}"
    elif os.getenv("DOCKER_USERNAME"):
        username_flag = "-u ".format(os.environ["DOCKER_USERNAME"])
    else:
        username_flag = ""

    if password is not None:
        password_flag = f"-p {password}"
    elif os.getenv("DOCKER_PASSWORD"):
        password_flag = "-p ".format(os.environ["DOCKER_PASSWORD"])
    else:
        password_flag = ""

    c.run(f"docker login {username_flag} {password_flag}".strip())


@task
def build_image(c):
    """Build and tag docker image."""
    version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    c.run(f"docker build -t knowsuchagency/covid-19:{version} .")
    c.run(
        f"docker tag knowsuchagency/covid-19:{version} knowsuchagency/covid-19:latest"
    )


@task(docker_login)
def push_image(c):
    """Push docker image to dockerhub."""
    c.run("docker push knowsuchagency/covid-19")


@task
def cdk_deploy(c):
    c.run("cdk deploy")


@task
def ecs_initialize(c):
    """Deploy the dockerfized app on aws ecs."""
    c.run(
        """
        ecs-preview init --project covid-19-api  \
          --app api                          \
          --app-type 'Load Balanced Web App' \
          --dockerfile './Dockerfile'        \
          --port 80                          \
          --profile ecs-admin                \
          --deploy
        """
    )


@task
def ecs_deploy(c):
    c.run("ecs-preview deploy")
