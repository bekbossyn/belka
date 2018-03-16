from . import common

from fabric.state import env
from fabric.decorators import task, hosts
from fabric.operations import sudo, run

env.repository = "https://github.com/bekbossyn/belka.git"
env.repo_name = "belka"


# @task
# def telecom():
#     env.user = "dev"
#     env.password = "root"
#     env.hosts = ["185.22.67.213"]

#
# @task
# def ocean():
#     env.user = "root"
#     env.password = "Truesight7"
#     env.hosts = ["159.65.203.197"]
#
#     run("cd /root/belka && git pull origin master")
#

@task
@hosts(['159.65.203.197'])
def restart():
    """
        updates repo, restarts the server
    """
    env.user = "root"
    env.password = "Truesight7"
    # env.hosts = ["159.65.203.197"]

    run("cd /root/belka && git pull origin master")

    run("cd /root/belka/ && . ./run.sh")
    sudo("systemctl restart gunicorn")
    sudo("systemctl restart nginx")
    common.update_supervisor()
