import requests
import subprocess
import signal
import time
from dotenv import dotenv_values
import sys
import sched

def get_commit_hash(user, repo, br):
    url = f"https://api.github.com/repos/{user}/{repo}/branches/{br}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        lHash = response.json()["commit"]["sha"]
        msg = response.json()["commit"]["commit"]["message"]
        return str(lHash)
    else:
        print(f"Failed to retrieve latest commit hash. Code: {response.status_code}")
        return None

def startBot():
    print(sys.executable)
    pHandle = subprocess.Popen(args=["python", "main.py"], executable=sys.executable)
    return pHandle


env_vars = dotenv_values(".env")


user = env_vars["STAGING_USER"]
repo = env_vars["STAGING_REPO"]
branch = env_vars["STAGING_BRANCH"]
shaPr = get_commit_hash(user, repo, branch) 

pHandle = startBot()

def check_for_new_commit(scheduler, pHandle, shaPr):
    print("oh boy! time to check github!")
    scheduler.enter(10,1,check_for_new_commit, (scheduler, pHandle, shaPr,))
    commit = get_commit_hash(user, repo, branch)
    sha = commit
    # new commit
    if (shaPr != sha):
        print(f"new commit on '{branch}': {sha[-4:]}; '{commit[1]}' - reloading bot")
        pHandle.send_signal(signal.SIGTERM)
        pHandle.wait()
        pHandle = startBot()
        shaPr = sha
    else:
        print("no new commit D:")


my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(float(env_vars["COMMIT_CHECK_INTERVAL"]), 1, check_for_new_commit, (my_scheduler, pHandle, shaPr))
print("running scheduled tasks!")
my_scheduler.run()
print("going to sleep now :)")

#while (True):
    # this code does not work and i am not sure why rn
    # could be useful later
    # bot is frozen
#    if (pHandle.poll() is not None):
#        print("bot dripped too hard, melting")
#        pHandle.send_signal(signal.SIGTERM)
#        pHandle.wait()
#        pHandle = startBot()
    
    # Check github every 60 seconds
