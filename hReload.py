import os

import requests
import subprocess
import signal
import time
from dotenv import dotenv_values
import sys
import sched


# Uses the GitHub API to extract the hash of the latest commit on a specific branch
# Requires STAGING_USER, STAGING_REPO, and STAGING_BRANCH
def get_commit_hash(user, repo, br, token):
    url = f"https://api.github.com/repos/{user}/{repo}/branches/{br}"
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "Frappe",
               "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        # Received OK HTTP code
        lHash = response.json()["commit"]["sha"]
        msg = response.json()["commit"]["commit"]["message"]
        return str(lHash)
    else:
        print(f"Failed to retrieve latest commit hash. Code: {response.status_code}")
        print(response.text)
        return None

# Opens a new process with thr same python interpreter for the discord bot
def startBot():
    pHandle = subprocess.Popen(args=["python", "main.py"], executable=sys.executable)
    return pHandle


env_vars = dotenv_values(".env")

user = env_vars["STAGING_USER"]
repo = env_vars["STAGING_REPO"]
branch = env_vars["STAGING_BRANCH"]
token = env_vars["PERSONAL_GITHUB_TOKEN"]

# Current latest commit
shaPr = get_commit_hash(user, repo, branch, token)

# pull latest commit
subprocess.call(["git", "remote", "add", "origin", f"git@github.com:{user}/{repo}"])
subprocess.call(["git", "fetch", "origin"])
subprocess.call(["git", "switch", branch])

# Start the bot
pHandle = startBot()

# Runs every COMMIT_CHECK_INTERVAL seconds and checks if a new commit has been pushed to the STAGING_BRANCH
# If so, it kills the bot process and restarts it
def check_for_new_commit(scheduler, pHandle, shaPr):
    print("oh boy! time to check github!")

    commit = get_commit_hash(user, repo, branch, token)
    sha = commit
    # new commit
    if (shaPr != sha):
        print(f"new commit on {branch}: {commit[1]} - reloading bot")
        pHandle.send_signal(signal.SIGTERM)
        pHandle.wait()

        ## Fetch the commit

        subprocess.call(["git", "pull"])

        pHandle = startBot()
        shaPr = sha
    else:
        print("no new commit D:")
    scheduler.enter(10, 1, check_for_new_commit, (scheduler, pHandle, shaPr,))




# Setup scheduler and schedule the commit check
my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(float(env_vars["COMMIT_CHECK_INTERVAL"]), 1, check_for_new_commit, (my_scheduler, pHandle, shaPr))
my_scheduler.run()

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
