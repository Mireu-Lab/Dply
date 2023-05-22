#!/bin/bash

cat asciiArt

if [ $(id -u) -ne 0 ]; then
    echo "\n\nplease run as root"
    exit
fi

echo "\n\n\n"

sudo apt-get update

distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y docker docker.io docker-compose nvidia-docker2
sudo systemctl restart docker


#SSH Container
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:debiansshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:fedorasshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:rockylinuxsshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:ubuntusshcontainer

#Jupyter Container
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterdebian
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterfedora
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu

docker-compose up --build -d

echo "Done!"