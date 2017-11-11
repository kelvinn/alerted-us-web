from fabric.api import env, run, local
from fabric.operations import put

IMAGE = "zephell/alerted-us-web"


def create(service): # Doesn't work yet
    env.user = 'core'
    if service == "web":
        run('sudo docker service create --name web zephell/alerted-us-web')

    if service == "db":
        run('sudo docker service create --name db mdillon/postgis')


def update():
    env.user = 'core'
    run('sudo docker service update webweb')


def deploy(version, service):
    """ deploy specified version of image to cluster """
    env.user = 'core'
    run('sudo docker service update --image %s:%s %s' % (IMAGE, version, service))
    print "Deployed %s:%s to %s" % (IMAGE, version, service)


def docker_clean():
    """ remove containers that have exited """
    env.user = 'core'
    run("docker rm `docker ps --no-trunc --all --quiet --filter=status=exited`")
