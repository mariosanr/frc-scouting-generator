import json
import pytz
import sys
import os.path
import eel

import constants
import apis.tba as tba_api
import excel_creation


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def parse_config_file():
     file = os.path.join(constants.base_directory, "config.json")
     with open(file, 'r') as config_file:
        config = json.load(config_file)
        tba_api.TBA_TOKEN = config['tba_token']
        constants.YEAR = config['year']
        constants.TEAM = config['team_name']
        constants.TEAM_CODE = config['team_code']
        constants.REGIONAL_NAME = config['event_name']
        constants.LANGUAGE = config['language'].lower()
        constants.TIMEZONE = config['timezone']
        constants.NUM_MATCHES_PER_TEAM = int(config['num_matches'])
        constants.REGIONAL_KEY = config['event_key']
        constants.SPREADSHEET_ID = config['spreadsheet_url']

        constants.OBSERVATIONS = config['observations']

        
        match(constants.LANGUAGE):
            case "en":
                constants.KEEP_OUT_FILE = "KEEP OUT"
            case "es":
                constants.KEEP_OUT_FILE = "NO TOCAR"
            case _:
                constants.LANGUAGE = "en"
                constants.KEEP_OUT_FILE = "KEEP OUT"
                print(f"Language '{config['LANGUAGE'].lower()}' is not supported. Only 'en' and 'es' are available. Reverting to the default 'en'")



        if constants.SPREADSHEET_ID:
            url = config['spreadsheet_url']
            idx1 = url.index('/d/')
            idx2 = url.index('/edit')
            constants.SPREADSHEET_ID = url[idx1 + len('/d/'): idx2]

        for section in constants.OBSERVATIONS:
            for observation in constants.OBSERVATIONS[section]:
                if observation == "__name__":
                    continue
                obs_type = constants.OBSERVATIONS[section][observation]['type']
                if obs_type in constants.ObservationType._member_names_:
                    constants.OBSERVATIONS[section][observation]['type'] = constants.ObservationType[obs_type]
                else:
                    print(f"Observation type {obs_type} does not exist")

        for sheet in config['sheets']:
            #the default id is 1 because 0 is the first sheet created, so this way it generates an error if the id has not been changed
            constants.SHEETS[sheet] = {'name': config['sheets'][sheet]['name'], 'id': '1'}
            if config['sheets'][sheet]['update']:
                constants.SHEETS_TO_UPDATE.append(sheet)


        if not constants.TIMEZONE and constants.REGIONAL_KEY and 'match_order' in constants.SHEETS_TO_UPDATE:
            response = tba_api.get_request(f"event/{constants.REGIONAL_KEY}")
            constants.TIMEZONE = response.json()['timezone']
            if constants.TIMEZONE not in pytz.all_timezones:
                try:
                    eel.print_error(f"The timezone '{constants.TIMEZONE}' provided by FRC for the event is not valid. Please specify the correct timezone manually")
                    return True
                except AttributeError:
                    print(f"The timezone '{constants.TIMEZONE}' provided by FRC for the event is not valid. Please specify the correct timezone manually")
                    sys.exit(0)
        return False



def main():
    return_again = parse_config_file()
    if return_again:
        return 400
    if not constants.REGIONAL_KEY:
        try:
            eel.print_error("You did not specify an event key. The following is a list of all the events your team is expected to attend:")
            tba_api.get_regionals()
            return 400
        except AttributeError:
            print("You did not specify an event key. The following is a list of all the events your team is expected to attend:")
            tba_api.get_regionals()
            sys.exit(0)

    if constants.TIMEZONE not in pytz.all_timezones and 'match_order' in constants.SHEETS_TO_UPDATE:
        try:
            eel.print_error(f"{constants.TIMEZONE} is an invalid timezone. Reverting to using the timezone provided by FRC for the event")
        except AttributeError:
            print(f"{constants.TIMEZONE} is an invalid timezone. Reverting to using the timezone provided by FRC for the event")
    if 'match_order' in constants.SHEETS_TO_UPDATE:
        try:
            eel.print_error(f"Using '{constants.TIMEZONE}' timezone")
        except AttributeError:
            print(f"Using '{constants.TIMEZONE}' timezone")

    try:
        eel.print_error('Changing existing spreadsheet...' if constants.SPREADSHEET_ID else 'Making new spreadsheet...')
    except AttributeError:
        print('Changing existing spreadsheet' if constants.SPREADSHEET_ID else 'Making new spreadsheet')
        print(f"The following sheets will be {'updated' if constants.SPREADSHEET_ID else 'created'}: {constants.SHEETS_TO_UPDATE}")
        if query_yes_no("Do you wish to continue?", default="yes") == False:
            sys.exit(0)
    

    if not constants.SPREADSHEET_ID:
        excel_creation.new_spreadsheet()
        return 201
    else:
        excel_creation.from_existing()
        return 200



if __name__ == "__main__":
    main()