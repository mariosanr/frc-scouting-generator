#################################################################################################################################
### The implementation of the GUI is done through the 'eel' tool. All copyrights to this tool go to Chris Knott,
### who is graciously distributing the project through the MIT License. 
### The complete license can be found here: https://github.com/python-eel/Eel/blob/main/LICENSE
### Special thanks to him and the team of contributors.
### The public repository for 'eel' can be found here: https://github.com/python-eel/Eel
#################################################################################################################################


import eel
import os.path
import json
import traceback
from importlib import reload

import constants
import main

eel.init('frontend')

@eel.expose
def config_exists():
    file = os.path.join(constants.base_directory, 'config.json')
    return os.path.exists(file)

@eel.expose
def get_JSON(path):
    file = os.path.join(constants.base_directory, path)
    with open(file, 'r') as config_file:
        config = json.load(config_file)
        return config


@eel.expose
def submit_JSON(obj, submit):
    global main, constants
    constants = reload(constants)
    main = reload(main)
    file = os.path.join(constants.base_directory, "config.json")
    with open(file, "w") as outfile:
        json.dump(obj, outfile, indent=4)
    if not submit:
        return 200
    eel.reset_console()()
    try:
        code = main.main()
        eel.set_spreadsheet_id(constants.SPREADSHEET_ID)()
        return code
    except Exception as err:
        traceback_str = traceback.format_exc()
        eel.print_error(traceback_str)
        print(traceback_str)
        return 500

eel.start('index.html', port=0)