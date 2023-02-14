import requests
import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from conf import headers, graphql
import logging
import argparse
import re

SCOPES = ["https://www.googleapis.com/auth/calendar"]

parser = argparse.ArgumentParser(
    description="Insert your PlayHQ fixture into your Google calendar."
)

parser.add_argument("url", type=str, help="Fixture URL")
arguments = parser.parse_args()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

# Game length in minutes
game_length = 45


def get_team_parameters(url: str):
    """Parses the URL and grabs the necessary attributes for the GraphQL request

    Args:
        url (str): PlayHQ URL
    """
    parsed = re.findall(
        r"https://www.playhq.com/(.*)/org/.*/(.*)", url, flags=re.IGNORECASE
    )[0]
    tenant = parsed[0]
    team_id = parsed[1]
    return tenant, team_id


def calendar_login():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def main(team_url):

    service = calendar_login()

    tenant, team_id = get_team_parameters(url=team_url)

    variables = {"teamID": team_id}

    headers.headers["tenant"] = tenant

    web = requests.post(
        url="https://api.playhq.com/graphql",
        json={"query": graphql.graphql, "variables": variables},
        headers=headers.headers,
    )

    results = json.loads(web.text)["data"]["discoverTeamFixture"]

    calendar_events = (
        service.events()
        .list(calendarId="primary", q="PlayHQ-GraphQL-Scraper")
        .execute()
    )

    for i in results:

        if i["fixture"]["games"]:
            start_time = datetime.strptime(
                f"{i['provisionalDate']}T{i['fixture']['games'][0]['allocation']['time']}",
                "%Y-%m-%dT%H:%M:%S",
            )

            end_time = start_time + timedelta(minutes=game_length)

            game = i["fixture"]["games"][0]

            venue_name = game["allocation"]["court"]["venue"]["name"]
            court_number = game["allocation"]["court"]["name"]
            round = i["name"]
            grade = i["grade"]["name"]
            away_team = game["away"]["name"]
            home_team = game["home"]["name"]

            summary = f"Basketball - {round} {venue_name} {court_number}"

            individual_event = {
                "summary": summary,
                "location": venue_name,
                "description": f"""{round} - {grade}
{home_team} VS {away_team}
Basketball at {venue_name} on {court_number}

PlayHQ-GraphQL-Scraper""",
                "start": {
                    "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "timeZone": "Australia/Melbourne",
                },
                "end": {
                    "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "timeZone": "Australia/Melbourne",
                },
            }

        elif i["fixture"]["byes"]:
            logging.info(f"{round} is a Bye")
            continue

        new = True

        for event in calendar_events["items"]:
            if summary == event["summary"]:
                new = False
                logging.info(f"{round} {summary} is already in your calendar")
                continue

        if new:
            logging.info(f"Adding {summary} to your calendar")
            service.events().insert(
                calendarId="primary", body=individual_event
            ).execute()


if __name__ == "__main__":
    main(arguments.url)
