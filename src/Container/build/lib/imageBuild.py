from src.error import ERROR
from src.setting import DockerClient

def repoImageBuild(self) -> bool:
    status = 500  # 컨테이너 생성 실패시 변경

    try:
        f = open("./Setting/dockerfile", "r", encoding="utf-8")
        dockerfile = f.read().format(self.containerImage)

        w = open(f"./Projects/{self.gitRepo[2]}/Dockerfile", "w", encoding="utf-8")
        w.write(dockerfile)
        w.close()

        DockerClient.images.build(
            path=f"./Projects/{self.gitRepo[2]}",
            dockerfile=f"./Projects/{self.gitRepo[2]}" + "/Dockerfile",
            tag=f"{self.gitRepoURL}:latest",
        )

        status = 200
    
    except:
        ERROR.Logging()
        status = 500  # 컨테이너 생성 실패시 변경
    
    return {"status": status, "imageTag": f"{self.gitRepoURL}:latest",}
