- Install dependencies using ``pip install -r requirements.txt``
- Create a ".env" file and paste the below text into it, placing the necessary info where specified

  ```
    APPLICATION_KEY=\\BOT TOKEN\\
    GUILD_ID=\\ID OF A TEST GUILD FOR INSTANT SLASH COMMANDS\\
    STAGING_USER =\\GITHUB USERNAME ASSOCIATED WITH HOTLOAD REPO\\
    STAGING_REPO=\\NAME OF REPO BEING CHECKED FOR HOT RELOADING\\
    STAGING_BRANC=\\BRANCH YOU WOULD LIKE TO CHECK FOR HOT RELOADING\\
```
  
- Run with hot reloading: `hReload.py`(make sure to edit repo details in the source code for now)
- Run normally: `main.py`
