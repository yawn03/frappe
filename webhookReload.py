from subprocess import Popen

from dotenv import dotenv_values
from flask import Flask, request

import hReload

app = Flask(__name__)

env_vars = dotenv_values(".env")
branch = env_vars["STAGING_BRANCH"]
pHandle: Popen = hReload.startBot()


@app.route("/update", methods=["POST"])
def update():
    print(request.json)
    try:
        if request.json["ref"] == ("refs/heads/" + branch):
            print("good update")
            global pHandle
            pHandle = hReload.reset_bot(pHandle)
            return "received!"
    except:
        print("not a push or not correct branch")
        return "received!"

    return "received!"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)

