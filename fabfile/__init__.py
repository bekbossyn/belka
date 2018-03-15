from . import common

from fabric.state import env
from fabric.decorators import task

env.repository = "https://github.com/bekbossyn/belka.git"
env.repo_name = "belka"


# @task
# def telecom():
#     env.user = "dev"
#     env.password = "root"
#     env.hosts = ["185.22.67.213"]


@task
def ocean():
    env.user = "root"
    env.password = "Truesight7"
    env.hosts = ["159.65.203.197"]
