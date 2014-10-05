Vagrant.configure("2") do |config|
  ## Chose your base box
  ## Add the box with: vagrant box add precise64 http://files.vagrantup.com/precise64.box
  #config.vm.box = "precise64"
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.network "forwarded_port", guest: 443, host: 443
  config.vm.network "forwarded_port", guest: 2223, host: 2223  # For InfluxDB testing
  config.vm.network "forwarded_port", guest: 8000, host: 8000  # For Django Dev server
  config.vm.network "forwarded_port", guest: 8888, host: 8888  # For ipython notebook

  ## Use all the defaults:
  # config.vm.provision :salt do |salt|

  #  salt.minion_config = "salt/minion"
  #  salt.run_highstate = true

  #end

  require 'rbconfig'
  is_windows = (RbConfig::CONFIG['host_os'] =~ /mswin|mingw|cygwin/)
  if is_windows
    # Provisioning configuration for shell script.

    config.vm.provision "shell" do |sh|
      sh.path = "provisioning/windows.sh"
      sh.args = "provisioning/site.yml provisioning/inventory provisioning/group_vars"
    end
  else
    # Provisioning configuration for Ansible (for Mac/Linux hosts).
    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/playbook.yml"
      #ansible.inventory_path = "provisioning/inventory"
      ansible.sudo = true
    end
  end

  #config.vm.provision "ansible" do |ansible|
  #  ansible.verbose = "v"
  #  ansible.playbook = "provision-dev-ansible.yml"
  #end

  #config.vm.provision "shell",
  #  inline: "apt-get update"

  #config.vm.provision "docker" do |d|
  #  d.build_image "/vagrant",
  #    args: "-t 'web'"
  #  d.pull_images "jamesbrink/postgresql"
  #  d.pull_images "dockerfile/redis"
  #  d.run "dockerfile/redis",
  #    args: "-t 'redis'"
  #  d.run "jamesbrink/postgresql",
  #    args: "-t 'db' -e 'RACK_ENV=development' -e 'USER=docker' -e 'PASSWORD=docker' -e 'SCHEMA=docker'"
  #end

  # add a bit more memory, it never hurts. It's VM specific and we're using Virtualbox here.
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 2048]
  end
end
