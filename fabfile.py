from fabric.api import run
from fabric.api import env

IMAGE = "zephell/alerted-us-web"

def deploy(version, service_name):
    """ deploy specified version of image to cluster """
    run('docker service update --image %s:%s %s' % (IMAGE, version, service_name))
    print "Deployed %s:%s to %s" % (IMAGE, version, service_name)

def docker_clean():
    """ remove containers that have exited """
    run("docker rm `docker ps --no-trunc --all --quiet --filter=status=exited`")
