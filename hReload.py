import requests
import subprocess
import signal
import time

def get_commit_hash(user, repo, br):
    url = f"https://api.github.com/repos/{user}/{repo}/branches/{br}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        lHash = response.json()["commit"]["sha"]
        msg = response.json()["commit"]["commit"]["message"]
        return [lHash, msg]
    else:
        print(f"Failed to retrieve latest commit hash. Code: {response.status_code}")
        return None


def startBot():
    pHandle = subprocess.Popen(['python3', 'main.py'], stdout=subprocess.PIPE)
    return pHandle


user = "NeoRubylith"
repo = "frappe"
branch = "main"
shaPr = get_commit_hash(user, repo, branch) 

pHandle = startBot()

while (True):
    # code was broken
    # bot is frozen
#    if (pHandle.poll() is None):
#        print("bot dripped too hard, melting")
#        pHandle.send_signal(signal.SIGTERM)
#        pHandle.wait()
#        pHandle = startBot()
    
    # Check github every 60 seconds
    if ((time.time() % 60) == 0):
        commit = get_commit_hash(user, repo, branch)
        sha = commit[0]
        # new commit
        if (shaPr != sha):
            print(f"new commit on '{branch}': {sha[-4:]}; '{commit[1]}' - reloading bot")
            pHandle.send_signal(signal.SIGTERM)
            pHandle.wait()
            pHandle = startBot()
            shaPr = sha
