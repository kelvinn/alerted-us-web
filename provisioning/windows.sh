#!/bin/bash
#
# Windows shell provisioner for Ansible playbooks, based on KSid's
# windows-vagrant-ansible: https://github.com/KSid/windows-vagrant-ansible
#
# @todo - Allow proxy configuration to be passed in via Vagrantfile config.
#
# @see README.md
# @author Jeff Geerling, 2014
# @author Kelvin Nicholson, 2014 (modifications)
# @version 1.0
#


ANSIBLE_PLAYBOOK=$1
ANSIBLE_HOSTS=$2
ANSIBLE_GROUP_VARS=$3
VAGRANT_ANSIBLE_HOSTS="/etc/ansible/hosts"
VAGRANT_GROUP_VARS="/etc/ansible/"

if [ ! -f /vagrant/$ANSIBLE_PLAYBOOK ]; then
  echo "Cannot find Ansible playbook."
  exit 1
fi

if [ ! -f /vagrant/$ANSIBLE_HOSTS ]; then
  echo "Cannot find Ansible hosts."
  exit 2
fi

# Install Ansible and its dependencies if it's not installed already.
if [ ! -f /usr/bin/ansible ]; then
  echo "Installing pip via apt-get."
  apt-get install -y python python-dev python-pip libyaml-dev
  # Make sure setuptools are installed crrectly.
  pip install setuptools --no-use-wheel --upgrade
  echo "Installing required python modules."
  pip install paramiko pyyaml jinja2 markupsafe
  echo "Installing Ansible."
  pip install ansible
fi

[ -d /etc/ansible ] || mkdir /etc/ansible
cp /vagrant/${ANSIBLE_HOSTS} ${VAGRANT_ANSIBLE_HOSTS} && chmod -x ${VAGRANT_ANSIBLE_HOSTS}
cp -R /vagrant/${ANSIBLE_GROUP_VARS}/ ${VAGRANT_GROUP_VARS}
echo "Running Ansible provisioner defined in Vagrantfile."
ansible-playbook /vagrant/${ANSIBLE_PLAYBOOK} --inventory-file=${VAGRANT_ANSIBLE_HOSTS} --extra-vars "is_windows=true" --connection=local