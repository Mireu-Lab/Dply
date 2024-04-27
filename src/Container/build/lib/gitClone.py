from git import Git

def gitClone(self) -> bool:
    try:
        Git("./Project").clone(f"git@{self.gitRepo[0]}:{self.gitRepo[1]}/{self.gitRepo[2]}.git")
        return True
    
    except:
        return False