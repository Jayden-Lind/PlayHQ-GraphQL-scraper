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

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# team id can be grabbed from looking at your teams fixture, it is the last part of the URL
team_id = "80e27305"
# Game length in minutes
game_length = 45
tenant = "basketball-victoria"


def main():
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

    variables = {"teamID": team_id}

    headers.headers["tenant"] = tenant

    web = requests.post(
        url="https://api.playhq.com/graphql",
        json={"query": graphql.graphql, "variables": variables},
        headers=headers.headers,
    )
    result = json.loads(web.text)["data"]["discoverTeamFixture"]

    calendar_events = (
        service.events()
        .list(calendarId="primary", q="PlayHQ-GraphQL-Scraper")
        .execute()
    )

    for i in result:

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
    main()
