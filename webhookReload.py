import sys
import signal
import subprocess

from dotenv import dotenv_values
from flask import Flask, request


# used during initialization
def update_local_repo():
    # pull latest commit
    subprocess.call(["git", "remote", "add", "origin", f"git@github.com:{user}/{repo}"], stdout=subprocess.PIPE)
    subprocess.call(["git", "fetch", "origin"], stdout=subprocess.PIPE)
    subprocess.call(["git", "switch", branch], stdout=subprocess.PIPE)
    subprocess.call(["git", "reset", "--hard"], stdout=subprocess.PIPE)


def start_bot() -> subprocess.Popen:
    return subprocess.Popen(args=["python", "main.py"], executable=sys.executable)


def reset_bot(process) -> subprocess.Popen:
    print(f"new commit on {branch}")
    process.send_signal(signal.SIGTERM)
    process.wait()

    # Fetch the commit
    subprocess.call(["git", "pull"], stdout=subprocess.PIPE)

    return start_bot()


# webhook handling code
app = Flask(__name__)


# endpoint called on any push to repo
@app.route("/update", methods=["POST"])
def update():
    # check if the push was to the branch the hot reloader tracks
    if request.json["ref"] == ("refs/heads/" + branch):
        global pHandle
        pHandle = reset_bot(pHandle)

    # return something so GitHub doesn't give us an error
    return "received!"


if __name__ == '__main__':
    # grab environment variables
    env_vars = dotenv_values(".env")
    user = env_vars["STAGING_USER"]
    repo = env_vars["STAGING_REPO"]
    branch = env_vars["STAGING_BRANCH"]
    token = env_vars["PERSONAL_GITHUB_TOKEN"]

    update_local_repo()
    pHandle = start_bot()

    app.run(host="0.0.0.0", port=5555, debug=False)
