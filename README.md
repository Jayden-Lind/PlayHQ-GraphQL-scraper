# PlayHQ-GraphQL-Scraper

This allows you to obtain a list of upcoming games for a specific team in [PlayHQ](https://www.playhq.com/) and insert it into your calendar with the relevant information.

## Quick Example

```shell
PlayHQ-GraphQL-scraper$ git clone git@github.com:Jayden-Lind/PlayHQ-GraphQL-scraper.git
PlayHQ-GraphQL-scraper$ python3 -m venv venv
PlayHQ-GraphQL-scraper$ source venv/bin/activate
(venv) PlayHQ-GraphQL-scraper$ pip install -r requirements.txt
(venv) PlayHQ-GraphQL-scraper$ python google-calendar.py https://www.playhq.com/afl/org/frankston-bombers-football-netball-club/08986ec2/mpnfl-2023/teams/frankston-bombers-fnc-reserves/c852e16e
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=xxxxxxxxx&redirect_uri=xxxxx&scope=xxxxxxxx&access_type=offline
2023-02-14 23:19:02 INFO     Round 1 Basketball - Round 1 Bonbeach Reserve Oval 1 Bonbeach Reserve Oval 1 1 is already in your calendar
```


## Usage

1. Head to your teams fixture page on [PlayHQ](https://www.playhq.com/).
2. Copy the URL of the fixture page of your team and note this down for later

https://www.playhq.com/basketball-victoria/org/dandenong-basketball-association-inc/senior-domestic-summer-202223/teams/the-expendables/989925f7

3. Follow https://developers.google.com/calendar/api/quickstart/python by creating an external OAuth consent screen & a Desktop Client OAuth credential.
4. Download your client secret in a JSON file. Rename this to `credentials.json`.
5. In GCP Console -> APIs and Services -> OAuth consent screen -> Test users - add the calendar user that you wish to use this with.
6. Create new Python virtual environment ```python3 -m venv venv``` then activate it 

Linux: ```source venv/bin/activate```

Windows: ```venv\scripts\activate.bat```.

7. Install library requirements ```pip install -r requirements.txt```.
8. Initialise authentication by running ```python google-calendar.py```.

Open link that looks like below & sign in with your desired account and give permission to your calendar.

```shell
(venv) jayden@JD-Desktop:~/PlayHQ-GraphQL-scraper$ python google-calendar.py 
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=xxxxxxxxx&redirect_uri=xxxxx&scope=xxxxxxxx&access_type=offline
```

