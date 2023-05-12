from dotenv import dotenv_values
from flask import Flask, request

import hReload

app = Flask(__name__)

env_vars = dotenv_values(".env")
user = env_vars["STAGING_USER"]
repo = env_vars["STAGING_REPO"]
branch = env_vars["STAGING_BRANCH"]
token = env_vars["PERSONAL_GITHUB_TOKEN"]


@app.route("/update", methods=["POST"])
def update():
    print(request.json)
    if request.json["ref"] == ("refs/heads/" + branch):
        print("good update")
        global pHandle
        pHandle = hReload.reset_bot(pHandle)

    return "received!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
