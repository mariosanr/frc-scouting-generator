import constants
import apis.google as google_api
import populate_sheets


def create_spreadsheet(event_name):
  constants.SPREADSHEET_ID = google_api.create_spreadsheet(
    "Scouting{team}{name}{year}"
    .format(team = constants.TEAM, name = event_name, year = constants.YEAR)
    )
  sheet_names = [constants.SHEETS[sheet]['name'] for sheet in constants.SHEETS_TO_UPDATE]
  response = google_api.create_sheets(sheet_names, spreadsheet_id=constants.SPREADSHEET_ID)

  get_new_sheet_ids(response)
  write_sheet_ids(new_file=True)

  requests = []
  requests.append(
    {
      "updateSheetProperties": {
        "properties": {
          "sheet_id": 0,
          "title": constants.KEEP_OUT_FILE,
          "hidden": True,
        },
        "fields": "title,hidden"
      }
    }
  )

  google_api.writeBatchUpdates(requests, spreadsheet_id=constants.SPREADSHEET_ID)


def get_new_sheet_ids(api_response):
  replies = api_response['replies']
  dict_keys = list(constants.SHEETS.keys())
  dict_values = list(constants.SHEETS.values())
  for reply in replies:
    # get the key for the constants.SHEETS dictionary from the name of the sheet given in the reply from the google api
    sheet_key = dict_keys[dict_values.index({'name': reply['addSheet']['properties']['title'], 'id': '1'})]
    constants.SHEETS[sheet_key]['id'] = reply['addSheet']['properties']['sheetId']
  

def write_sheet_ids(new_file):
  table = []
  for key in constants.SHEETS:
    table.append([key, constants.SHEETS[key]['name'], constants.SHEETS[key]['id'] ])
  
  if not new_file:
    google_api.write(table, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.KEEP_OUT_FILE}'!A2")
  else:
    google_api.write(table, spreadsheet_id=constants.SPREADSHEET_ID, cell_range="A2") 


def check_changes_in_sheets():
   #get all the sheets 
  sheets = google_api.get_sheets(constants.SPREADSHEET_ID)

  #check if there are changes on the id or name
  changes = False

  dict_keys = list(constants.SHEETS.keys())
  dict_values = list(constants.SHEETS.values())
  dict_names = [sheet['name'] for sheet in dict_values]
  dict_ids = [sheet['id'] for sheet in dict_values]

  response_names = [sheet['properties']['title'] for sheet in sheets]
  response_ids = [str(sheet['properties']['sheetId']) for sheet in sheets]
  
  for i in range(len(dict_keys)):
     #check for a name change
     if dict_ids[i] in response_ids:
        idx = response_ids.index(dict_ids[i])
        if dict_names[i] != response_names[idx]:
           changes = True
           constants.SHEETS[dict_keys[i]]['name'] = response_names[idx]
     #check if sheet was deleted
     else:
        changes = True
        constants.SHEETS[dict_keys[i]]['id'] = '1'

  return changes


def simulate_quals():
  total_row_count = 2
  for section in constants.OBSERVATIONS:
    row_count = 0
    for observation in constants.OBSERVATIONS[section]:
      curr_row = total_row_count + row_count
      if observation == "__name__":
          continue
      match constants.OBSERVATIONS[section][observation]['type']:
          case constants.ObservationType.EVERY_MATCH:
              constants.COLS_W_OBSERVATIONS.append([observation, curr_row + constants.NUM_MATCHES_PER_TEAM])
              row_count += constants.NUM_MATCHES_PER_TEAM + 1
          case constants.ObservationType.YES_OR_NO:
              constants.COLS_W_OBSERVATIONS.append([observation, curr_row])
              row_count += 1
          case constants.ObservationType.OPTIONS:
              constants.COLS_W_OBSERVATIONS.append([observation, curr_row])
              row_count += 1
          case constants.ObservationType.PARAGRAPH:
              constants.COLS_W_OBSERVATIONS.append([observation, curr_row])
              row_count += 1
          case _:
              print("The observation type '{obs_type}' doesnt exist. If it should, please add the necessary framework".format(obs_type=constants.OBSERVATIONS[section][observation]['type']))
    total_row_count += row_count


def populate_sheet(name):
    if hasattr(populate_sheets, name):
      func = getattr(populate_sheets, name)
      func()
    else:
      print(f"Sheet {name} does not exist. Add a new function with the same name in populate_sheets.py")


def load_necessary_info():
  values = google_api.read(f"'{constants.KEEP_OUT_FILE}'!A1:D", constants.SPREADSHEET_ID)

  # get the number of teams and erase it from the table
  first_line = values.pop(0)
  num = int(first_line[0])
  constants.TEAM_TOTAL = num

  #get the sheet id for all sheets
  sheet_names = constants.SHEETS.keys()
  for value in values:
    if value[0] in sheet_names:
      constants.SHEETS[value[0]]['name'] = value[1]
      constants.SHEETS[value[0]]['id'] = value[2]
  
  #check if the ids or names have changed (if they erased a sheet or renamed it)
  changes = check_changes_in_sheets()

  # set the etags. first check if the sheet is deleted to know if the etag should be empty
  if constants.SHEETS['teams']['id'] != '1':
    constants.ETAG['TEAMS'] = first_line[1]
  if constants.SHEETS['match_order']['id'] != '1':
    constants.ETAG['MATCHES'] = first_line[2]
  if constants.SHEETS['advanced_stats']['id'] != '1':
    constants.ETAG['OPR'] = first_line[3]
  
  #create new sheets if updating non existent sheets
  sheets_to_create = []
  for sheet in constants.SHEETS_TO_UPDATE:
    if constants.SHEETS[sheet]['id'] == '1':
      sheets_to_create.append(constants.SHEETS[sheet]['name'])
  if sheets_to_create:
    response = google_api.create_sheets(sheets_to_create, spreadsheet_id=constants.SPREADSHEET_ID)
    get_new_sheet_ids(response)
    changes = True
  
  #write to keep out file if there were changes to the sheets
  if changes:
     write_sheet_ids(new_file=False)

  #recreate the cols_w_observations variable as if the quals sheet was updated
  if "quals" not in constants.SHEETS_TO_UPDATE and constants.SHEETS['quals']['id'] != '1':
    simulate_quals()



def from_existing():
  load_necessary_info()

  og_team_total = constants.TEAM_TOTAL
  og_etags = constants.ETAG.copy()

  for sheet in constants.SHEETS_TO_UPDATE:
    populate_sheet(sheet)

  #if changes were made
  if og_team_total != constants.TEAM_TOTAL or og_etags != constants.ETAG:
    values = [[str(constants.TEAM_TOTAL), constants.ETAG['TEAMS'], constants.ETAG['MATCHES'], constants.ETAG['OPR']]]
    google_api.write(values, constants.SPREADSHEET_ID, cell_range=f"'{constants.KEEP_OUT_FILE}'!A1")


def new_spreadsheet():
  create_spreadsheet(constants.REGIONAL_NAME)
  for sheet in constants.SHEETS_TO_UPDATE:
    populate_sheet(sheet)

  values = [[str(constants.TEAM_TOTAL), constants.ETAG['TEAMS'], constants.ETAG['MATCHES'], constants.ETAG['OPR']]]
  google_api.write(values, constants.SPREADSHEET_ID, cell_range=f"'{constants.KEEP_OUT_FILE}'!A1")


if __name__ == "__main__":
  load_necessary_info()