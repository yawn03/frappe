- Install dependencies using ``pip install -r requirements.txt``
- Create a ".env" file and paste the below text into it, placing the necessary info where specified

  ```
    APPLICATION_KEY=\\BOT TOKEN\\
    GUILD_ID=\\ID OF A TEST GUILD FOR INSTANT SLASH COMMANDS\\
    STAGING_USER =\\GITHUB USERNAME ASSOCIATED WITH HOTLOAD REPO\\
    STAGING_REPO=\\NAME OF REPO BEING CHECKED FOR HOT RELOADING\\
    STAGING_BRANCH=\\BRANCH YOU WOULD LIKE TO CHECK FOR HOT RELOADING\\
    COMMIT_CHECK_INTERVAL=\\TIME IN SECONDS\\
  ```
  
- Run with hot reloading: `hReload.py`(make sure to edit `.env` file :D)
- Run normally: `main.py`
