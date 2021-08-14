# PlayHQ-GraphQL-scraper
This allows you to obtain a list of upcoming games for a specific team in PlayHQ.

```google-calendar.py```
Lets you automatically populate it in your Google Calendar.

**Steps for Google Calendar:**

1. Obtain Team ID from URL of checking game. Team ID will look something like _aca061c8_.
2. Obtain Tenant which is _www.playhq.com/basketball-victoria_ basketball-victoria in this example.
3. Follow https://developers.google.com/calendar/api/quickstart/python to create an API KEY.
4. ```pip install -r requirements.txt```
5. Download "OAuth 2.0 Client IDs", save as credentials.json
6. ```python google-calendar.py``` and follow the steps.
