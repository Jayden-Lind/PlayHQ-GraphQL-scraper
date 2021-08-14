import requests
import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

#team id can be grabbed from looking at your teams fixture, it is the last part of the URL
team_id = ''
#Game length in minutes
game_length = 45
tenant = 'basketball-victoria'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    query = """query teamFixture($teamID: ID!) {\r\n  discoverTeamFixture(teamID: $teamID) {\r\n    id\r\n    name\r\n    provisionalDate\r\n    grade {\r\n      id\r\n      name\r\n      season {\r\n        id\r\n        name\r\n        competition {\r\n          id\r\n          name\r\n          organisation {\r\n            id\r\n            name\r\n            __typename\r\n          }\r\n          __typename\r\n        }\r\n        __typename\r\n      }\r\n      __typename\r\n    }\r\n    fixture {\r\n      ...RoundFixtureFragment\r\n      __typename\r\n    }\r\n    __typename\r\n  }\r\n}\r\n\r\nfragment RoundFixtureFragment on DiscoverRoundFixture {\r\n  byes {\r\n    ...DiscoverTeamFragment\r\n    __typename\r\n  }\r\n  games {\r\n    id\r\n    alias\r\n    pool {\r\n      id\r\n      name\r\n      __typename\r\n    }\r\n    away {\r\n      ...TeamFragment\r\n      __typename\r\n    }\r\n    home {\r\n      ...TeamFragment\r\n      __typename\r\n    }\r\n    result {\r\n      winner {\r\n        name\r\n        value\r\n        __typename\r\n      }\r\n      outcome {\r\n        name\r\n        __typename\r\n      }\r\n      home {\r\n        score\r\n        outcome {\r\n          name\r\n          value\r\n          __typename\r\n        }\r\n        statistics {\r\n          count\r\n          type {\r\n            value\r\n            __typename\r\n          }\r\n          __typename\r\n        }\r\n        __typename\r\n      }\r\n      away {\r\n        score\r\n        outcome {\r\n          name\r\n          value\r\n          __typename\r\n        }\r\n        statistics {\r\n          count\r\n          type {\r\n            value\r\n            __typename\r\n          }\r\n          __typename\r\n        }\r\n        __typename\r\n      }\r\n      __typename\r\n    }\r\n    status {\r\n      name\r\n      value\r\n      __typename\r\n    }\r\n    date\r\n    allocation {\r\n      time\r\n      court {\r\n        id\r\n        name\r\n        abbreviatedName\r\n        latitude\r\n        longitude\r\n        venue {\r\n          id\r\n          name\r\n          abbreviatedName\r\n          latitude\r\n          longitude\r\n          address\r\n          suburb\r\n          state\r\n          postcode\r\n          country\r\n          __typename\r\n        }\r\n        __typename\r\n      }\r\n      __typename\r\n    }\r\n    isStale\r\n    __typename\r\n  }\r\n  __typename\r\n}\r\n\r\nfragment TeamFragment on DiscoverPossibleTeam {\r\n  ... on ProvisionalTeam {\r\n    name\r\n    pool {\r\n      id\r\n      name\r\n      __typename\r\n    }\r\n    __typename\r\n  }\r\n  ... on DiscoverTeam {\r\n    ...DiscoverTeamFragment\r\n    __typename\r\n  }\r\n  __typename\r\n}\r\n\r\nfragment DiscoverTeamFragment on DiscoverTeam {\r\n  id\r\n  name\r\n  logo {\r\n    sizes {\r\n      url\r\n      dimensions {\r\n        width\r\n        height\r\n        __typename\r\n      }\r\n      __typename\r\n    }\r\n    __typename\r\n  }\r\n  season {\r\n    id\r\n    name\r\n    competition {\r\n      id\r\n      name\r\n      __typename\r\n    }\r\n    __typename\r\n  }\r\n  organisation {\r\n    id\r\n    name\r\n    type\r\n    __typename\r\n  }\r\n  __typename\r\n}\r\n"""

    variables = {"teamID": team_id}

    headers = {
        'authority': 'api.playhq.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': '*/*',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'tenant': tenant,
        'content-type': 'application/json',
        'origin': 'https://www.playhq.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-AU,en-US;q=0.9,en-GB;q=0.8,en;q=0.7'
    }


    web = requests.post('https://api.playhq.com/graphql', json={'query': query, 'variables' : variables}, headers=headers)
    result = json.loads(web.text)['data']['discoverTeamFixture']

    for i in result:
        start_time = datetime.strptime(f"{i['provisionalDate']}T{i['fixture']['games'][0]['allocation']['time']}", '%Y-%m-%dT%H:%M:%S')
        end_time = start_time + timedelta(minutes = game_length)


        event = {
                'summary': f"Basketball @ {i['fixture']['games'][0]['allocation']['court']['venue']['name']}, {i['fixture']['games'][0]['allocation']['court']['name']}",
                'location': i['fixture']['games'][0]['allocation']['court']['venue']['name'],
                'description': 'Basketball',
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Australia/Melbourne',
            }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()


if __name__ == '__main__':
    main()