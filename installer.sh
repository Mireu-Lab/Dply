#!/bin/sh

pythonInstall() {
    echo "\n\n++ Python Install\n\n"
    sudo apt-get update
    sudo apt-get install python3.10 python3-pip
}

dockerInstall() {
    echo "\n\n++ Docker Install\n\n"

    sudo apt-get update
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update
    sudo apt-get install -y docker docker.io docker-compose nvidia-docker2
    sudo systemctl restart docker
}

dockerSSHImage() {
    echo "\n\n++ SSH Container Pull\n\n"

    #SSH Container Image
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:centossshcotainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:ubuntusshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:rockylinuxsshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:tensorflowsshcontainer

	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpucentossshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpuubuntusshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpurockylinuxsshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gputensorflowsshcontainer
}

dockerJupyterImage() {
    echo "\n\n++ Jupyter Container Pull\n\n"

    #Jupyter Container Image
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytercentos
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytertensorflow
    
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytercentos
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterubuntu
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytertensorflow
}

dockerDataBaseImage() {
    echo "\n\n++ Database Container Pull\n\n"

    # Database Container Image
    docker pull mysql:latest
    docker pull mariadb:latest
    docker pull mongo:latest
    docker pull redis:latest
}

gpuSetting() {
    pip3 install tensorflow
    cat install/gpuSetting

    python3 src/install.py

    pip3 uninstall tensorflow -y
}

cat install/asciiArt

if [ $(id -u) -ne 0 ]; then
    echo "\n\nplease run as root"
    exit
fi


if cat /etc/issue | grep -q -e Ubuntu -e ubuntu ; then
    pythonInstall
    dockerInstall

    gpuSetting

    dockerSSHImage
    dockerJupyterImage
    dockerDataBaseImage
    
    echo "\n\n\n+Complete basic system installation"

    docker-compose up -d
    rm env/.env

    echo "Done!"
else
    echo "\n\nUnsupported OS."
fi
