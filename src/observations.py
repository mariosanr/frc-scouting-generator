import apis.google as google_api
import constants

def every_match(num_matches, sheet_id, startColumn, endColumn, startRow, endRow):
    length_added = num_matches + 1

    formula = ('=IF(SUM(INDIRECT("RC[-{num}]", FALSE):INDIRECT("RC[-1]", FALSE))=0,0,TRIMMEAN(INDIRECT("RC[-{num}]", FALSE):INDIRECT("RC[-1]", FALSE),(1/{num})*2))'
               .format(num=num_matches))
    
    return [google_api.create_formula_request(formula, sheet_id, startColumn, endColumn, startRow, endRow),
            length_added]


def yes_or_no(sheet_id, startColumn, endColumn, startRow, endRow):
    length_added = 1
    return [{
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": startRow,
                "endRowIndex": endRow,
                "startColumnIndex": startColumn,
                "endColumnIndex": endColumn
            },
            "rule": {
                "condition": {
                    "type": 'ONE_OF_LIST',
                    "values": [
                        {"userEnteredValue": 'Si' if constants.LANGUAGE == 'es' else 'Yes'},
                        {"userEnteredValue": 'No'},
                    ],
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    },
    length_added
    ]


def options(optionsList, sheet_id, startColumn, endColumn, startRow, endRow):
    length_added = 1

    values = []
    for option in optionsList:
        values.append({"userEnteredValue": option})
    return [{
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": startRow,
                "endRowIndex": endRow,
                "startColumnIndex": startColumn,
                "endColumnIndex": endColumn
            },
            "rule": {
                "condition": {
                    "type": 'ONE_OF_LIST',
                    "values": values,
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    },
    length_added
    ]


def paragraph():
    length_added = 1
    return [{}, length_added]


if __name__ == "__main__":
    pass