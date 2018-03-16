from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.state import env

env.repository = "https://github.com/bekbossyn/belka.git"
env.repo_name = "belka"

@task
def git_pull():
    """
    Updates the repository
    """

    env.user = "root"
    env.password = "Truesight7"
    env.hosts = ["159.65.203.197"]

    run("cd /root/belka && git pull origin master")


# @task
# def celery_logs():
#     """
#     Updates the repository
#     """
#     sudo("tail -f /var/log/celery/belka.log")


@task
def update_supervisor():
    # sudo("cp ~/{}/configs/supervisor/celery.conf /etc/supervisor/conf.d".format(env.repo_name))
    # sudo("supervisorctl reread; supervisorctl restart celery; supervisorctl restart celerybeat; supervisorctl restart flower; supervisorctl update; supervisorctl status celery")
    sudo("supervisorctl update")


@task
def update():
    """
    Restarts server
    """
    run("cd /root/belka/ && . ./run.sh")
    sudo("systemctl restart gunicorn")
    sudo("systemctl restart nginx")
    update_supervisor()
