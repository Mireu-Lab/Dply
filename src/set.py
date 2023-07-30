import datetime
import subprocess

def time() -> float:
    return datetime.datetime.now().timestamp()

def GPURange() -> int | None:
    try:
        cmd = """nvidia-smi --query-gpu=index --format=csv,noheader"""
        lists = str(subprocess.check_output(cmd, shell=True).decode('utf-8')).split("\n")
        return int(max(lists))+1

    except subprocess.CalledProcessError:
        return None


def GPUCheck() -> bool:
    try:
        cmd = """nvidia-smi --query-gpu=index --format=csv,noheader"""
        lists = str(subprocess.check_output(cmd, shell=True).decode('utf-8')).split("\n")
        
        return True if int(max(lists))+1 >= 1 else False
            
        
    except subprocess.CalledProcessError:
        return False
