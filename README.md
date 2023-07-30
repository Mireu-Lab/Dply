# Container Build Management Mastering Program

<br><br>

# Install

The libraries installed by the program are as follows.

- [curl](#curl)
- [python3](#python)
- [python3-pip](#python)
- [docker](#docker)
- [docker-compose](#docker)
- [nvidia-docker2](#nvidia-docker)

<br><br>

> Additionally, the system only supports the **Ubuntu** OS and is not compatible with other operating systems.

To run this program, the following programs need to be installed using the provided commands.



## Curl

```shell
sudo apt-get install curl
```



## Docker

```
sudo apt-get install docker\
                 docker.io\
                 docker-compose
```



## Python

```shell
sudo apt-get install python3\
                 python3-pip
```



## Nvidia Docker (optional)

```shell
sudo apt-get update
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```





# Container

This program deploys development environment containers using Docker API, so you need to install Container Images locally from the source. The installation process is as follows:



## CPU

```shell
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:centossshcotainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:ubuntusshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:rockylinuxsshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:tensorflowsshcontainer

docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytercentos
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterubuntu
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupyterrockylinux
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:containerjupytertensorflow
```



## GPU (optional)

```shell
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpucentossshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpuubuntusshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gpurockylinuxsshcontainer
docker pull registry.gitlab.com/container-images4/docker-ssh-conteiner:gputensorflowsshcontainer

docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytercentos
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterubuntu
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupyterrockylinux
docker pull registry.gitlab.com/container-images4/docker-jupyter-container:gpucontainerjupytertensorflow
```



## DataBase

```
docker pull mysql:latest 
docker pull mariadb:latest
docker pull mongo:latest
docker pull redis:latest
```

Note: Installer support will be provided in future updates.



# API Run

In this version, the completeness of the API may be low.

Also, the program is structured into CPU and GPU versions, so please execute the API based on your environment.

```shell
docker volume create dply_program_sqlvolume

docker run -d \
    --name dply-program \
    -p 8080:80 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v dply_program_sqlvolume:/API/SQL \
    -v /var/log/dply:/API/Log \
    registry.gitlab.com/individual-projects2/container-build-management-mastering-program:api
```



# Remove

Before executing the command, please check if the container is working or if the data has been backed up. The following command will delete containers, volumes, and networks created by Dply.

```shell
sudo sh remove.sh
```



# API v0.0.2

The program is implemented as FastAPI and information can be obtained through Docs in FastAPI.
The FastAPI connection method is as follows.

> http://[IP]:8080/docs

<br>

The functions supported by the API are implemented as follows.

- [Build](#build) #Deploy project containers
- [Status](#status) #Change the status of the project container
- [Delete](#delete) #Delete Project
- [Search](#search) #Project information

<br>

## Build

The API is a program for deploying development environment containers.\
The parameters required to use the API are as follows.

|    Variable Name | Type | Default | Description |
| :----------: | :--: | :-----: | :-------------------------------------------: |
| projectName | str | - | Project Name |
|  Processor | str | CPU | Processor Allocation Parameters |
|      OS | str | Ubuntu | Development Environment Container Operating System Allocation Parameters |
|     Type | str | Jupiter | Development Environment Container Access Method Allocation Parameters |
|   Password | str | None | Project Distribution Container Password Allocation Parameters |
| databaseList | list | None | Database Container Deployment Allocation Parameters |

<br>

The result is output as shown below.

<br>

The API also specifies the types that it supports.\
The specified type is configured as follows.

| Variable Name | Type | Support Type (Case Check) |
| :------------: | :----: | :----------------------------: |
| Processor    | str  | CPU, GPU                     |
| OS           | str  | ubuntu, centos, rockylinux, tensorflow   |
| Type         | str  | SSH, Jupyter                 |
| databaseList | list | mysql, mariadb, mongo, redis |

<br>

You have to check the case and enter the college to avoid errors.\
In addition, these character interpretations are implemented without a separate filter.

### Status Code

#### Status Code 200

The error was successfully distributed

```json
{
    "devContainer": {
        "status": int,
        "port": int
    },
    "databaseContainer": [
        {
            "database": str,
            "status": bool
        },
        ...
    ]
}
```


#### Status Code 400

The corresponding error may occur when the Docker Image is not Full.
Run the installer again and process it.

```json
{
    "msg": "You do not have permission.",
    "NotBuildContainer": "The name is already registered."
}
```


#### Status Code 503

The error is an error that occurs when the project name is duplicated.
Try again by changing the project name to another one.

```json
{
    "msg": "You do not have permission.",
    "NotBuildContainer": "The name is already registered."
}
```

<br><br>

#### Status Code 403

This error is an error that occurs when the computing system attempts to assign an unprovided processor.

```json
{
  "msg": "You do not have permission.",
  "SystemProcessorConfigurationError": "Your system does not support the processor you want. Please select a different processor."
}
```

<br><br>


## Status

This function is a program for managing the execution of project containers.\
The parameters required to use the API are as follows.

<br>

|   Variable Name | Type | Default | Description |
| :---------: | :--: | :----: | :-----------: |
| projectName | str | - | Project Name |
| statusSetting | str | - | Project Container Status Information |

<br>

The result is output as shown below.

<br><br>

### Status Code
#### Status Code 200

```json
{
    "Status": {
        "devContainer": bool,
        "databaseContainer": {
            str: bool,
            ...
        }
    },
}
```

<br><br>

#### Status Code 404

```json
{
    "msg": "Not found",
    "NotFoundProjects": "Projects that cannot be found"
}
```

<br><br>


## Delete

The API is a program for deleting development environment containers.

The parameters required to use the API are as follows.

|   Variable Name | Type | Default | Description |
| :---------: | :--: | :----: | :-----------: |
| projectName | str | - | Project Name |

The result value is output as follows.

<br><br>

### Status Code
#### Status Code 200

Project Delete Results

```json
{
    "projectName": str,
    "projectStatus": {
        "devContainer": bool,
        "databaseContainers": {
            str: bool,
            ...
        },
        "containersNetwork": bool,
        "containersVolume": bool
    },
}
```

<br><br>

#### Status Code 404

If a project has already been deleted or is missing

```json
{
    "msg": "Not found",
    "NotFoundProjects": "Projects that cannot be found"
}
```

<br><br>

## Search

The API is a program for deleting development environment containers.\
The parameters required to use the API are as follows.

|   Variable Name | Type | Default | Description |
| :---------: | :--: | :----: | :-----------: |
| projectName | str | None | Project Name |


The function will also print **single project information** if the value 'projectName' is entered and **multiple project information** if not entered.

The result is output as shown below.

<br><br>

### Status Code

#### Status Code 200

- [Single Project Information](#single-project-information)
- [Multiple Project Information](#multiple-project-information)
- [No data from multiple project information](#no-data-from-multiple-project-information)

<br><br>

##### Single Project Information

```json
{
    "projectName": str,
    "createdTimes": float,
    "devContainer": {
        "type": str,
        "gpu": bool,
        "status": bool,
        "port": int,
    },
    "databaseContainers": {
        str: {
            "status": bool,
            "ip": str,
        },
        ...
    }
}
```

<br>

##### Multiple Project Information

```json
[
    {
        "projectName": str,
        "devContainer": {
            "Type": str,
            "status": bool,
            "port": int,
            "gpu": int,
            "createdTimes": float,
        },
        "databaseContainer": [
            str,
            ...
        ],
    },
    ...
]
```

<br>

##### No data from multiple project information

```json
[]
```


### Status Code 404

Project information not found

```json
{
    "msg": "Not found",
    "NotFoundProjects": "Projects that cannot be found"
}
```