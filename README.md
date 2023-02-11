# PlayHQ-GraphQL-Scraper
This allows you to obtain a list of upcoming games for a specific team in [PlayHQ](https://www.playhq.com/) and insert it into your calendar with the relevant information.

```google-calendar.py```
Lets you automatically populate it in your Google Calendar.

**Steps for Google Calendar:**

1. Obtain Team ID from URL of checking game. Team ID will look something like _aca061c8_.
2. Obtain Tenant which is _www.playhq.com/basketball-victoria_ **basketball-victoria** in this example.
3. Follow https://developers.google.com/calendar/api/quickstart/python.
4. Create an external OAuth consent screen.
5. Create a "Desktop Client" OAuth credential.
6. Download your client secret in a JSON file. Rename this to `credentials.json`.
7. In GCP Console -> APIs and Services -> OAuth consent screen -> Test users, add the user you want to use.
9. Create new Python virtual environment ```python3 -m venv venv``` then activate it Linux: ```source venv/bin/activate``` OR Windows: ```venv\scripts\activate.bat```
10. Install library requirements```pip install -r requirements.txt```.
11. Initialise authentication by running ```python google-calendar.py```.

Open link that looks like below & sign in with your desired account and give permission to 

```shell
(venv) jayden@JD-Desktop:~/PlayHQ-GraphQL-scraper$ python google-calendar.py 
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=xxxxxxxxx&redirect_uri=xxxxx&scope=xxxxxxxx&access_type=offline
```