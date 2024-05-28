import os.path
import traceback
import eel


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import constants


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

google_creds = None
google_service = None


def create_token():
  cred_file = os.path.join(constants.base_directory, "credentials.json")
  flow = InstalledAppFlow.from_client_secrets_file(
      cred_file, SCOPES
  )
  return flow.run_local_server(port=0)


def authenticate():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  token_file = os.path.join(constants.base_directory, "token.json")
  if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      creds = create_token()
    # Save the credentials for the next run
    with open(token_file, "w") as token:
      token.write(creds.to_json())
  
  global google_creds, google_service
  google_creds = creds
  google_service = build("sheets", "v4", credentials=google_creds)
  return creds


def create_spreadsheet(title):
  
  spreadsheet = {"properties": {"title": title,
                                "defaultFormat":{"horizontalAlignment": 2,"wrapStrategy": 3}}}
  spreadsheet = (
      google_service.spreadsheets()
      .create(body=spreadsheet, fields="spreadsheetId")
      .execute()
  )
  try:
    eel.print_error(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
  except AttributeError:
    print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
  return spreadsheet.get("spreadsheetId")



def create_sheets(names, spreadsheet_id):
  requests = []

  for title in names:
    requests.append(
        {
            "addSheet": {
                "properties": {"title": title}
            }
        }
    )

  return writeBatchUpdates(requests, spreadsheet_id=spreadsheet_id)


def create_formula_request(formula, sheet_id, startColumn, endColumn, startRow, endRow):
  return {
    "repeatCell": {
      "range": {
        "sheetId": sheet_id,
        "startRowIndex": startRow,
        "endRowIndex": endRow,
        "startColumnIndex": startColumn,
        "endColumnIndex": endColumn
      },
      "cell": {
          "userEnteredValue":{
              "formulaValue": formula
          }
        },
      "fields": "userEnteredValue"
    }
  }


def writeBatchUpdates(request_body, spreadsheet_id):
  try:
    body = {"requests": request_body}
    response = (
        google_service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )

    return response
  except HttpError as error:
    traceback_str = traceback.format_exc()
    try:
      eel.print_error(traceback_str)
    except AttributeError:
      print(error)
    return error


def get_sheets(spreadsheet_id):
  result = (
        google_service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id)
        .execute()
    )
  sheets = result.get('sheets', '')
  return sheets


def read(cell_range, spreadsheet_id):
  try:
    result = (
        google_service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=cell_range)
        .execute()
    )
    values = result.get('values', [])
    try:
      eel.print_error(f"{len(values)} rows retrieved from {cell_range}")
    except AttributeError:
      print(f"{len(values)} rows retrieved from {cell_range}")
    return values
  
  except HttpError as error:
    traceback_str = traceback.format_exc()
    try:
      eel.print_error(traceback_str)
    except AttributeError:
      print(error)
    return [[]]


#df needs to be a list of lists
#to achieve this with a pandas df you can do df.values.tolist() before passing it as a parameter
def write(df, spreadsheet_id, cell_range, value_input_option="USER_ENTERED"):
  try:
    body = {"values": df}
    result = (
        google_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=cell_range,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    try:
      eel.print_error(f"{result.get('updatedCells')} cells updated in {cell_range}.")
    except AttributeError:
      print(f"{result.get('updatedCells')} cells updated in {cell_range}.")
    return result
  
  except HttpError as error:
    traceback_str = traceback.format_exc()
    try:
      eel.print_error(traceback_str)
    except AttributeError:
      print(error)
    return error


authenticate()

if __name__ == "__main__":
  create_spreadsheet("TestSpreadsheet")