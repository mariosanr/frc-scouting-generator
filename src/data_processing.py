import pandas as pd
import numpy as np

import constants
import apis.statbotics as statbotics_api
import apis.google as google_api
import apis.tba as tba_api


def get_stats(event_key):
    response = statbotics_api.get_event_info(event_key)
    return response.json()

def get_stats_from_excel(cell_range):
    df = pd.DataFrame(google_api.read(cell_range, constants.SPREADSHEET_ID))
    df.columns = ['team', 'total_epa', 'total_epa_sd', 'auto_epa', 'auto_epa_sd', 'teleop_epa', 'teleop_epa_sd', 'endgame_epa', 'endgame_epa_sd']
    df['team'] = df['team'].astype(np.int64)
    return df

def clean_stats(stats_json):
    data = []
    for team in stats_json:
        data.append(
            {
                'team': team['team'],
                'team_name': team['team_name'],
                'total_epa': team['epa']['breakdown']['total_points']['mean'],
                'total_epa_sd': team['epa']['breakdown']['total_points']['sd'],
                'auto_epa': team['epa']['breakdown']['auto_points']['mean'],
                'auto_epa_sd': team['epa']['breakdown']['auto_points']['sd'],
                'teleop_epa': team['epa']['breakdown']['teleop_points']['mean'],
                'teleop_epa_sd': team['epa']['breakdown']['teleop_points']['sd'],
                'endgame_epa': team['epa']['breakdown']['endgame_points']['mean'],
                'endgame_epa_sd': team['epa']['breakdown']['endgame_points']['sd'],
            }
        )

    df = pd.DataFrame.from_dict(data)
    df['team'] = df['team'].astype(np.int64)
    return df
    

def get_blue_alliance_stats():
    response = tba_api.get_request("event/{key}/oprs".format(key = constants.REGIONAL_KEY), etag_name='OPR')
    if response == 304:
        values = google_api.read(f"'{constants.SHEETS['advanced_stats']['name']}'!A1:M{constants.TEAM_TOTAL + 1}", constants.SPREADSHEET_ID)
        columns = values.pop(0)
        df = pd.DataFrame(values, columns=columns)
        df = df[['team', 'opr', 'dpr', 'ccwm']]
        df['team'] = df['team'].astype(np.int64)

        return df
    
    df = pd.DataFrame(response.json())
    if not df.empty:
        df.reset_index(inplace=True)
        df.columns = ['team', 'ccwm', 'dpr', 'opr']
        df = df[['team', 'opr', 'dpr', 'ccwm']]
        df['team'] = df['team'].str[3:]
        df['team'] = df['team'].astype(np.int64)

        return df
    return None



def get_advanced_stats():
    #uncomment the following line if you already have the data stored on the sheet
    #df = get_stats_from_excel(f"'{constants.SHEETS['advanced_stats']['name']}'!A2:J45")
    #comment the following 2 lines if getting the stats directly from the excel
    stats = get_stats(constants.REGIONAL_KEY)
    df = clean_stats(stats)
    tba_stats_df = get_blue_alliance_stats()
    if tba_stats_df is not None:
        df = df.merge(tba_stats_df, how='left', on='team')
        values = [df.columns.tolist()]
    # FIXME I added the values definitions inside the if and else, have not tried it.
    else:
        values = [df.columns.tolist()]
        values[0].extend(['opr', 'dpr', 'ccwm'])
        
    df.fillna(0, inplace=True)

    values.extend(df.values.tolist())
    return values


if __name__ == "__main__":
    get_advanced_stats()
