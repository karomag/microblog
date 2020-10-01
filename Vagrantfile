$install = <<~INSTALL
  echo Download Poetry...
  sudo -u vagrant curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -o /home/vagrant/get-poetry.py
  echo Installing Poetry...
  sudo -u vagrant python3 /home/vagrant/get-poetry.py
  echo Installed successfully
INSTALL
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.provision "shell", inline: $install
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
end