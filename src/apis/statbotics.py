import constants
import requests
import eel

STATBOTICS_URL = "https://api.statbotics.io/v3/"

def get_event_info(event_key):
    url = "{base}team_events?event={key}".format(base=STATBOTICS_URL, key=event_key)
    payload={}
    headers = {}

    response = requests.request("GET", url=url, headers=headers, data=payload)

    if response.status_code != 200:
        try:
            eel.print_error(response.headers)
        except AttributeError:
            print(response.headers)
        raise RuntimeError(f"Request '{url}' was unsuccessful with code: {response.status_code}")
    
    return response

if __name__ == "__main__":
    get_event_info(constants.REGIONAL_KEY)