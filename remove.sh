#!/bin/sh

removeSetting() {
    echo "\n\n++ Container Remove\n\n"

    pip3 install docker
    python3 remove.py
    pip3 uninstall docker

    rm -rf /etc/dply /var/log
}

dockerImageRemove() {
    echo "\n\n++ Docker Images Remove\n\n"

    #SSH Container Image
    docker rmi registry.gitlab.com/individual-projects2/container-build-management-mastering-program:api\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:centossshcotainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:ubuntusshcontainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:rockylinuxsshcontainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:tensorflowsshcontainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:gpucentossshcontainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:gpuubuntusshcontainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:gpurockylinuxsshcontainer\
                registry.gitlab.com/container-images4/docker-ssh-conteiner:gputensorflowsshcontainer\
                registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytercentos\
                registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu\
                registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux\
                registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytertensorflow\
                registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytercentos\
                registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterubuntu\
                registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterrockylinux\
                registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytertensorflow\
                mysql:latest\
                mariadb:latest\
                mongo:latest\
                redis:latest
}

cat remove/remove

if [ $(id -u) -ne 0 ]; then
    echo "\n\nplease run as root"
    exit
fi

docker-compose down

removeSetting
dockerImageRemove

echo "\n\n\nDone!"