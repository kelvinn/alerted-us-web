from fabric.api import run
from fabric.api import env
from dockerfabric.apiclient import docker_fabric

env.docker_tunnel_local_port = 22024

IMAGE = "zephell/alerted-us-web"
SERVICE = "alerted-us-web-staging"

def deploy(version):
    """ deploy specified version of image to cluster """
    run('docker service update --image %s:%s %s' % (IMAGE, version, SERVICE))
    print "Deployed %s:%s to %s" % (IMAGE, version, SERVICE)

def docker_clean():
    """ remove containers that have exited """
    run("docker rm `docker ps --no-trunc --all --quiet --filter=status=exited`")
