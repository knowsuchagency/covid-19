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
