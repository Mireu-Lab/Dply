import docker

DockerClient = docker.DockerClient()

for containerID in DockerClient.containers.list():
    if (containerID.id).startswith(f"Build_Management_"):
        DockerClient.containers.get(containerID.id).stop()
        DockerClient.containers.get(containerID.id).remove()

for containerID in DockerClient.networks.list():
    if (containerID.id).startswith(f"Build_Management_"):
        DockerClient.networks.get(containerID.id).remove()

for containerID in DockerClient.volumes.list():
    if (containerID.id).startswith(f"Build_Management_"):
        DockerClient.volumes.get(containerID.id).remove()