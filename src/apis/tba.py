import requests
import eel

import constants

TBA_TOKEN = ""
TBA_URL = "https://www.thebluealliance.com/api/v3/"


def get_request(url, etag_name=''):
  etag = ''
  if etag_name:
    etag = constants.ETAG[etag_name]
    
  payload={}
  headers = {
    'X-TBA-Auth-Key': TBA_TOKEN,
    'If-None-Match': etag
  }

  url = TBA_URL + url

  response = requests.request("GET", url=url, headers=headers, data=payload)

  try:
    if etag_name:
      constants.ETAG[etag_name] = response.headers['ETag']
  except KeyError:
    pass

  # no new data
  if response.status_code == 304:
    return response.status_code

  if response.status_code != 200:
    try:
      eel.print_error(response.headers)
    except AttributeError:
      print(response.headers)
    raise RuntimeError(f"Request '{url}' was unsuccessful with code: {response.status_code}")

  return response


def get_regionals():
  response = get_request("team/{team_code}/events/{year}/simple".format(team_code = "frc" + constants.TEAM_CODE, year = constants.YEAR))

  for event in response.json():
    try:
      eel.print_error("City: {city},  Event: {name},  Event Key: {key}".format(city=event['city'], name=event['name'], key=event['key']))
    except AttributeError:
      print("City: {city},  Event: {name},  Event Key: {key}".format(city=event['city'], name=event['name'], key=event['key']))

