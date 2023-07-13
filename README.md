# Container Build Management Mastering Program

<br><br>

# Install

The library installed by the program is as follows.

- python3
- python3-pip
- docker
- nvidia-docker2
- docker-compose

<br><br>

> In addition, the OS supported by the system is **Ubuntu**, which is not supported by other OSes.


The execution code is as follows.
```bash
$ sudo sh install.sh
```

# Remove

Please check again whether the container is working or the data has been subtracted before executing the command.\
This command deletes containers, volumes, and networks created by Dply.

```
sudo sh remove.sh
```

# API v0.0.1

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