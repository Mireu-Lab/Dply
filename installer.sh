#!/bin/sh

pythonInstall() {
    sudo apt-get update
    sudo apt-get install python3 python3-pip
}

dockerInstall() {
    sudo apt-get update
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update
    sudo apt-get install -y docker docker.io docker-compose nvidia-docker2
    sudo systemctl restart docker
}

dockerSSHImage() {
    #SSH CPU Container Image
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:debiansshcontainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:fedorasshcontainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:rockylinuxsshcontainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:ubuntusshcontainer
}

dockerJupyterImage() {
    #Jupyter CPU Container Image
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterdebian
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterfedora
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu

    #Jupyter GPU Container Image
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpucentossshcontainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpurockylinuxsshcontainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpuubuntusshcontainer
}

dockerJupyterImage() {
    #Jupyter CPU Container Image
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterfedora
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu

    #Jupyter GPU Container Image
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytercentos
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterubuntu
}

dockerDataBaseImage() {
    # Database Container Image
    docker pull mysql:latest
    docker pull mariadb:latest
    docker pull mongo:latest
    docker pull redis:latest
}


cat asciiArt

if [ $(id -u) -ne 0 ]; then
    echo "\n\nplease run as root"
    exit
fi


if cat /etc/issue | grep -q -e Ubuntu -e ubuntu ; then
    pythonInstall
    dockerInstall

    dockerSSHImage
    dockerJupyterImage
    dockerDataBaseImage

    echo "\n\n\n+Complete basic system installation"

    docker-compose up --build -d

    echo "Done!"
else
    echo "\n\nUnsupported OS."
fi
