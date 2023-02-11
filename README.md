# PlayHQ-GraphQL-Scraper
This allows you to obtain a list of upcoming games for a specific team in [PlayHQ](https://www.playhq.com/).

```google-calendar.py```
Lets you automatically populate it in your Google Calendar.

**Steps for Google Calendar:**

1. Obtain Team ID from URL of checking game. Team ID will look something like _aca061c8_.
2. Obtain Tenant which is _www.playhq.com/basketball-victoria_ **basketball-victoria** in this example.
3. Follow https://developers.google.com/calendar/api/quickstart/python to create an OAuth 2.0 Client.
4. Download your client secret in a JSON file. Rename this to `credentials.json`.
5. In GCP Console -> APIs and Services -> OAuth consent screen -> Test users.
6. Add the user that you wish to use this application with.
7. ```pip install -r requirements.txt```.
8. ```python google-calendar.py``` and authorise the application you created in step 3.
