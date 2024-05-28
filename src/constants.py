from enum import Enum
import os

base_directory = os.path.dirname(os.path.dirname( __file__ ))

class ObservationType(Enum):
    EVERY_MATCH = 1
    YES_OR_NO = 2
    OPTIONS = 3
    PARAGRAPH = 4


TEAM_CODE = ""
TEAM = ""
YEAR = ""

LANGUAGE = None
TIMEZONE = None
NUM_MATCHES_PER_TEAM = None

# Total number of teams present in the regional
TEAM_TOTAL = 0

OBSERVATIONS = {}
COLS_W_OBSERVATIONS = []
SHEETS = {}
SHEETS_TO_UPDATE = []

REGIONAL_NAME = ""
REGIONAL_KEY = ""

#The id appears in the url between spreadsheets/d/ and /edit
SPREADSHEET_ID = ""

KEEP_OUT_FILE = ""

ETAG = {
    "TEAMS": '',
    "MATCHES": '',
    "OPR": '',
}