import requests
import json
from conf import graphql, headers


def main(team_id="", tenant=""):

    variables = {"teamID": team_id}

    headers.headers["tenant"] = tenant

    graphql_query = requests.post(
        url="https://api.playhq.com/graphql",
        json={"query": graphql.graphql, "variables": variables},
        headers=headers.headers,
    )

    result = json.loads(graphql_query.text)["data"]["discoverTeamFixture"]

    for i in result:
        print_str = f"{i['name']} - {i['provisionalDate']} "
        if i["fixture"]["games"]:
            print(
                print_str
                + i["fixture"]["games"][0]["allocation"]["time"]
                + " "
                + i["fixture"]["games"][0]["allocation"]["court"]["venue"]["name"]
                + " "
                + i["fixture"]["games"][0]["allocation"]["court"]["name"]
                + " "
                + i["fixture"]["games"][0]["home"]["name"]
                + " VS "
                + i["fixture"]["games"][0]["away"]["name"]
                + " "
            )
        else:
            print(print_str + f"BYE")


main(team_id="80e27305", tenant="basketball-victoria")
