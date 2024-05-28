from datetime import datetime
import pytz
import eel

import constants
import apis.google as google_api
import apis.tba as tba_api
import observations
import sheets_aesthetics
import data_processing

def teams():
    match(constants.LANGUAGE):
        case "en":
            header = [['Number', 'Team', 'School', 'Scout']]
        case "es": 
            header = [['Numero', 'Equipo', 'Escuela', 'Responsable']]

    response = tba_api.get_request(f"event/{constants.REGIONAL_KEY}/teams", etag_name='TEAMS')
    if response == 304:
        try:
            eel.print_error(f"There was nothing to update in sheet '{constants.SHEETS['teams']['name']}'")
        except AttributeError:
            print(f"There was nothing to update in sheet '{constants.SHEETS['teams']['name']}'")
        return

    values_dict = response.json()
    values = header
    for x in values_dict:
        value = []
        value.append(x['team_number'])
        equipo = x['nickname']
        index = equipo.find('PrepaTec - ')
        if index != -1:
            equipo = equipo[11:]
        index = equipo.find('Prepa Tecmilenio - ')
        if index != -1:
            equipo = equipo[19:]
        value.append(equipo)
        value.append(x['school_name'])
        value.append(' ')
        values.append(value)

    constants.TEAM_TOTAL = len(values) - 1
    
    try:
        eel.print_error(f"Number of teams in the event: {constants.TEAM_TOTAL}")
        eel.print_error(f"Populating sheet '{constants.SHEETS['teams']['name']}'")
    except AttributeError:
        print(f"Number of teams in the event: {constants.TEAM_TOTAL}")
        print(f"Populating sheet '{constants.SHEETS['teams']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['teams']['name']}'!A1")
    sheets_aesthetics.aesthetic_teams()


def match_order():
    timezone = pytz.timezone(constants.TIMEZONE)

    match(constants.LANGUAGE):
        case "en":
            header = [['Match', 'Red Alliance', '' , '', 'Blue Alliance', '' , '', 'Date and Time']]
        case "es": 
            header = [['Match', 'Alianza Roja', '' , '', 'Alianza Azul', '' , '', 'Dia y Hora']]

    response = tba_api.get_request(f"event/{constants.REGIONAL_KEY}/matches/simple", etag_name="MATCHES")
    if response == 304:
        try:
            eel.print_error(f"There was nothing to update in sheet '{constants.SHEETS['match_order']['name']}'")
        except AttributeError:
            print(f"There was nothing to update in sheet '{constants.SHEETS['match_order']['name']}'")
        return

    values_dict = response.json()
    
    values = header
    match_dict = {}
    for x in values_dict:
        if x['comp_level'] != 'qm':
            continue
        value = []
        value.append('Quals {num}'.format(num=x['match_number']))
        for team in x['alliances']['red']['team_keys']:
            value.append(team[3:])
        for team in x['alliances']['blue']['team_keys']:
            value.append(team[3:])
        date = datetime.fromtimestamp(x['time'], tz=timezone)
        date = date.strftime("%a %I:%M%p")
        value.append(date)

        match_dict[x['match_number']] = value
    
    for i in range(1, len(match_dict) + 1):
        values.append(match_dict[i])
    
    try:
        eel.print_error(f"Populating sheet '{constants.SHEETS['match_order']['name']}'")
    except AttributeError:
        print(f"Populating sheet '{constants.SHEETS['match_order']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['match_order']['name']}'!A1")
    sheets_aesthetics.aesthetic_match_order()


def quals():
    sheet_id = constants.SHEETS['quals']['id']
    
    table = google_api.read(cell_range=f"'{constants.SHEETS['teams']['name']}'!A1:B", spreadsheet_id=constants.SPREADSHEET_ID)
    values = [['', '']]
    values.extend(table)

    total_row_count = 2
    requests = []
    aes_requests = []

    for section in constants.OBSERVATIONS:
        row_count = 0
        upper_header = []
        for observation in constants.OBSERVATIONS[section]:
            curr_row = total_row_count + row_count
            if observation == "__name__":
                upper_header.append(constants.OBSERVATIONS[section][observation])
                continue
            match constants.OBSERVATIONS[section][observation]['type']:
                case constants.ObservationType.EVERY_MATCH:
                    num = constants.NUM_MATCHES_PER_TEAM
                    response = observations.every_match(num, sheet_id, curr_row + num, curr_row + num + 1, 2, len(values))
                    constants.COLS_W_OBSERVATIONS.append([observation, curr_row + num])
                    requests.append(response[0])
                    row_count += response[1]
                    temp_list = [i for i in range(1, num + 1)]
                    temp_list.append(observation)
                    values[1].extend(temp_list)
                case constants.ObservationType.YES_OR_NO:
                    response = observations.yes_or_no(sheet_id, curr_row, curr_row + 1, 2, len(values))
                    constants.COLS_W_OBSERVATIONS.append([observation, curr_row])
                    requests.append(response[0])
                    row_count += response[1]
                    values[1].append(observation)
                case constants.ObservationType.OPTIONS:
                    response = observations.options(constants.OBSERVATIONS[section][observation]['options'], sheet_id, curr_row, curr_row + 1, 2, len(values))
                    constants.COLS_W_OBSERVATIONS.append([observation, curr_row])
                    requests.append(response[0])
                    row_count += response[1]
                    values[1].append(observation)
                case constants.ObservationType.PARAGRAPH:
                    response = observations.paragraph()
                    constants.COLS_W_OBSERVATIONS.append([observation, curr_row])
                    row_count += response[1]
                    values[1].append(observation)
                case _:
                    print("Observation type '{t}' does not exist. If it should, please add all that is necessary".format(t=constants.OBSERVATIONS[section][observation]['type']))
            
        upper_header.extend(['' for _ in range(row_count - 1)])
        values[0].extend(upper_header)
        aes_requests.append(sheets_aesthetics.merge_cells(sheet_id, total_row_count, total_row_count + row_count, 0, 1))
        total_row_count += row_count


    try:
        eel.print_error(f"Populating sheet '{constants.SHEETS['quals']['name']}'")
    except AttributeError:
        print(f"Populating sheet '{constants.SHEETS['quals']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['quals']['name']}'!A1")
    google_api.writeBatchUpdates(requests, spreadsheet_id=constants.SPREADSHEET_ID)
    sheets_aesthetics.aesthetic_quals(aes_requests)


def scouting():
    sheet_id = constants.SHEETS['scouting']['id']

    formula = f"""=ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(TRANSPOSE(VLOOKUP($B$1,'{constants.SHEETS['match_order']['name']}'!$A$2:$G,{{2,3,4,5,6,7}},0)),"")), 6, 1)"""
    match(constants.LANGUAGE):
        case "en":
            values = [['Match', 'Quals 1'], 
                      [''],
                      ['Red Alliance', formula],
                      [''],
                      [''],
                      ['Blue Alliance']]
        case "es": 
            values = [['Partida', 'Quals 1'], 
                      [''],
                      ['Alianza Roja', formula],
                      [''],
                      [''],
                      ['Alianza Azul']]
    
    try:
        eel.print_error(f"Populating sheet '{constants.SHEETS['scouting']['name']}'")
    except AttributeError:
        print(f"Populating sheet '{constants.SHEETS['scouting']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['scouting']['name']}'!A1")

    formula = f"""=IFERROR(VLOOKUP($B3,'{constants.SHEETS['teams']['name']}'!$A$2:$D,4,0),"")"""
    requests = []
    requests.append(google_api.create_formula_request(formula, sheet_id, 2, 3, 2, 8) )
    requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 1,
                "endColumnIndex": 2
            },
            "rule": {
                "condition": {
                    "type": 'ONE_OF_RANGE',
                    "values": [
                        {"userEnteredValue": f"='{constants.SHEETS['match_order']['name']}'!$A2:$A"}
                    ],
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })
    google_api.writeBatchUpdates(requests, spreadsheet_id=constants.SPREADSHEET_ID)

    sheets_aesthetics.aesthetic_scouting()
    

def advanced_stats():
    sheet_id = constants.SHEETS['advanced_stats']['id']

    values = data_processing.get_advanced_stats()
    try:
        eel.print_error(f"Populating sheet '{constants.SHEETS['advanced_stats']['name']}'")
    except AttributeError:
        print(f"Populating sheet '{constants.SHEETS['advanced_stats']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['advanced_stats']['name']}'!A1")
    sheets_aesthetics.aesthetic_advanced_stats()


def ranking():
    sheet_id = constants.SHEETS['ranking']['id']
    quals_exists = False if constants.SHEETS['quals']['id'] == '1' else True

    match(constants.LANGUAGE):
        case "en":
            header = ['Code', 'Team', 'EPA', 'OPR', 'DPR', 'CCWM']
            if quals_exists:
                upper_header = ['', '', 'Advanced Stats', '', '', '', 'Manual Scouting']
                for col in constants.COLS_W_OBSERVATIONS:
                    header.append(col[0])
            else:
                upper_header = ['', '', 'Advanced Stats']
            header.append('Available')
        case "es": 
            header = ['Numero', 'Equipo', 'EPA', 'OPR', 'DPR', 'CCWM']
            if quals_exists:
                upper_header = ['', '', 'Estadisticas Avanzadas', '', '', '', 'Scouting Manual']
                for col in constants.COLS_W_OBSERVATIONS:
                    header.append(col[0])
            else:
                upper_header = ['', '', 'Estadisticas Avanzadas']
            header.append('Disponible')
            
    
    #advanced stats
    sheet_name = constants.SHEETS['advanced_stats']['name']
    general_formula_cell = '$A3'
    col_nums = [2, 3, 11, 12, 13]
    f_formula = """=IFERROR(VLOOKUP({cell},'{sheet_name}'!$A$2:$P,{col_num},0), "")"""

    requests = []
    curr_row = 1

    #The formulas for advanced stats are created
    for col in col_nums:
        formula = f_formula.format(sheet_name=sheet_name, cell=general_formula_cell, col_num=col)
        requests.append(google_api.create_formula_request(formula, sheet_id, curr_row, curr_row+1, 2, constants.TEAM_TOTAL + 2) )
        curr_row += 1

    if quals_exists:
        #manual scouting
        sheet_name = constants.SHEETS['quals']['name']
        col_limit = sheets_aesthetics.num_to_A1(constants.COLS_W_OBSERVATIONS[-1][1])
        f_formula = """=IFERROR(VLOOKUP({cell},'{sheet_name}'!$A$3:${col_limit},{col_num},0), "")"""

        #The formulas for the manual scouting are created
        for col in constants.COLS_W_OBSERVATIONS:
            formula = f_formula.format(sheet_name=sheet_name, col_limit=col_limit, cell=general_formula_cell, col_num=col[1]+1)
            requests.append(google_api.create_formula_request(formula, sheet_id, curr_row, curr_row+1, 2, constants.TEAM_TOTAL + 2) )
            curr_row += 1

    #add the "Available" column prefilled with true
    formula = "=TRUE"
    requests.append(google_api.create_formula_request(formula, sheet_id, curr_row, curr_row+1, 2, constants.TEAM_TOTAL + 2) )


    values = [
        upper_header,
        header
    ]

    team_nums = google_api.read(cell_range=f"'{constants.SHEETS['teams']['name']}'!A2:A", spreadsheet_id=constants.SPREADSHEET_ID)
    values.extend(team_nums)

    try:
        eel.print_error(f"Populating sheet '{constants.SHEETS['ranking']['name']}'")
    except AttributeError:
        print(f"Populating sheet '{constants.SHEETS['ranking']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['ranking']['name']}'!A1")
    google_api.writeBatchUpdates(requests, spreadsheet_id=constants.SPREADSHEET_ID)
    sheets_aesthetics.aesthetic_ranking()


def compare():
    sheet_id = constants.SHEETS['compare']['id']
    quals_exists = False if constants.SHEETS['quals']['id'] == '1' else True

    #advanced stats
    sheet_name = constants.SHEETS['advanced_stats']['name']
    cell_name = 'B$1'
    col_nums = [2, 3, 11, 12, 13]
    f_formula = """=IFERROR(VLOOKUP({cell},'{sheet_name}'!$A$2:$P,{col_num},0), "{comment}")"""


    match(constants.LANGUAGE):
        case "en":
            values = [
                ['Teams', constants.TEAM_CODE], [''],
                ['EPA'], ['OPR'], ['DPR'], ['CCWM'],
                [''],
            ]
        case "es": 
            values = [
                ['Equipos', constants.TEAM_CODE], [''],
                ['EPA'], ['OPR'], ['DPR'], ['CCWM'],
                [''],
            ]

    if quals_exists:
        for col in constants.COLS_W_OBSERVATIONS:
            values.append([col[0]])

    # The formulas for the avanced stats are created
    for i in range(len(col_nums)):
        comment = "Team not found" if i == 0 else ""
        formula = f_formula.format(sheet_name=sheet_name, cell=cell_name, col_num=col_nums[i], comment=comment)
        values[i+1].append(formula)
    curr_row = len(col_nums) + 1
    
    if quals_exists:
        curr_row += 1

        #manual scouting
        sheet_name = constants.SHEETS['quals']['name']
        col_limit = sheets_aesthetics.num_to_A1(constants.COLS_W_OBSERVATIONS[-1][1])
        f_formula = """=IFERROR(VLOOKUP({cell},'{sheet_name}'!$A$3:${col_limit},{col_num},0), "")"""

        #the formulas for the manual scouting are created
        for col in constants.COLS_W_OBSERVATIONS:
            formula = f_formula.format(sheet_name=sheet_name, col_limit=col_limit, cell=cell_name, col_num=col[1]+1)
            values[curr_row].append(formula)
            curr_row += 1

    requests = []
    requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 1,
                "endColumnIndex": 2
            },
            "rule": {
                "condition": {
                    "type": 'ONE_OF_RANGE',
                    "values": [
                        {"userEnteredValue": f"='{constants.SHEETS['teams']['name']}'!$A2:$A"}
                    ],
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })
    requests.append({
        "autoFill": {
            "useAlternateSeries": True,
            "sourceAndDestination": {
                "source": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": curr_row,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2
                },
                "dimension": "COLUMNS",
                "fillLength": 2
            }
        }
    })

    try:
        eel.print_error(f"Populating sheet '{constants.SHEETS['compare']['name']}'")
    except AttributeError:
        print(f"Populating sheet '{constants.SHEETS['compare']['name']}'")
    google_api.write(values, spreadsheet_id=constants.SPREADSHEET_ID, cell_range=f"'{constants.SHEETS['compare']['name']}'!A1")
    google_api.writeBatchUpdates(requests, spreadsheet_id=constants.SPREADSHEET_ID)
    sheets_aesthetics.aesthetics_compare()


if __name__ == "__main__":
    #quals('2024mxmo')
    pass