import docker

DockerClient = docker.DockerClient()

for containerID in DockerClient.containers.list():
    if (containerID.name).startswith(f"Build_Management_"):
        DockerClient.containers.get(str(containerID.id)).stop()
        DockerClient.containers.get(str(containerID.id)).remove()

for containerID in DockerClient.networks.list():
    if (containerID.name).startswith(f"Build_Management_"):
        DockerClient.networks.get(str(containerID.name)).remove()

for containerID in DockerClient.volumes.list():
    if (containerID.name).startswith(f"Build_Management_"):
        DockerClient.volumes.get(str(containerID.name)).remove()