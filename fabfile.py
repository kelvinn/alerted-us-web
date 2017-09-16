from fabric.api import env, run

env.user = 'ubuntu'


def create_database():
    run('dokku postgres:create hellodjango-database')
    run('dokku postgres:link hellodjango-database hellodjango')