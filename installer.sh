#!/bin/bash

programDefaultInstall()
{
    echo "\n\n++ Python Install\n\n"
    sudo apt-get update
    sudo apt-get install python3.10 python3-pip dialog
}

dockerInstall(){
    sudo apt-get install -y docker docker.io docker-compose 

    sudo usermod -aG docker $USER
    sudo systemctl restart docker
}

nvidiaDockerInstall(){
    echo "\n\n++ Docker Install\n\n"

    sudo apt-get update
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update
    sudo apt-get install -y nvidia-docker2
    sudo systemctl restart docker
}

dockerCPUImagePull(){
    echo "\n\n++ CPU SSH Container Pull\n\n"
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:centossshcotainer
    docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:ubuntusshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:rockylinuxsshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:tensorflowsshcontainer

    echo "\n\n++ CPU Jupyter Container Pull\n\n"
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytercentos
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytertensorflow
}


dockerCPUImagePull(){
    echo "\n\n++ GPU SSH Container Pull\n\n"
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpucentossshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpuubuntusshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpurockylinuxsshcontainer
	docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gputensorflowsshcontainer

    echo "\n\n++ GPU Jupyter Container Pull\n\n"
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytercentos
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterubuntu
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterrockylinux
    docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytertensorflow
}

dockerDataBaseImage(){
    echo "\n\n++ Database Container Pull\n\n"

    # Database Container Image
    docker pull mysql:latest 
    docker pull mariadb:latest
    docker pull mongo:latest
    docker pull redis:latest
}

gpuSetting(){
    pip3 install tensorflow==2.4.0
    clear

    cat install/gpuSetting

    python3 src/install.py

    clear
    pip3 uninstall tensorflow==2.4.0 -y
}

programVersion() {
    while choice=$(dialog --title "$TITLE" \
                    --menu "Please select a program type" 10 40 3 1 "CPU" 2 "GPU" \
                    2>&1 >/dev/tty)
        do
            case $choice in
                1) 
                    break;;
                2) 
                    gpuSetting
                    nvidiaDockerInstall
                    break;;
                *)
                    break;;
            esac
        done
    clear
}

cat install/asciiArt

if [ $(id -u) -ne 0 ]; then
    echo "\n\nplease run as root"
    exit
fi


if cat /etc/issue | grep -q -e Ubuntu -e ubuntu ; then
    programDefaultInstall
    dockerInstall
    clear

    programVersion

    dockerSSHImage
    clear
    dockerJupyterImage
    clear
    dockerDataBaseImage
    clear

    echo "\n\n\n+Complete basic system installation"

    # docker-compose up -d
    # rm env/.env

    echo "Done!"
else
    echo "\n\nUnsupported OS."
fi
