import constants
import apis.google as google_api


def aesthetic_teams():
    sheet_id = constants.SHEETS['teams']['id']
    requests = [
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 4
                }
            }
        },
    ]
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 1
                },
            },
            "fields": "gridProperties.frozenRowCount"
        }
    })

    return google_api.writeBatchUpdates(requests, constants.SPREADSHEET_ID)


def aesthetic_match_order():
    sheet_id = constants.SHEETS['match_order']['id']
    requests = [merge_cells(sheet_id, 1, 4, 0, 1), merge_cells(sheet_id, 4, 7, 0, 1)]
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 1
                },
            },
            "fields": "gridProperties.frozenRowCount"
        }
    })

    return google_api.writeBatchUpdates(requests, constants.SPREADSHEET_ID)


def aesthetic_quals(requests):
    sheet_id = constants.SHEETS['quals']['id']

    requests.append(
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                }
            }
        }
    )
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 2,
                    "frozenColumnCount": 2,
                },
            },
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
        }
    })

    formula = f"""=IFERROR(VLOOKUP($A3,'{constants.SHEETS['teams']['name']}'!$A$2:$B,2,0), "Team does not exist")"""
    requests.append(google_api.create_formula_request(formula, sheet_id, 1, 2, 2, constants.TEAM_TOTAL + 2) )
    

    return google_api.writeBatchUpdates(requests, spreadsheet_id=constants.SPREADSHEET_ID)


def aesthetic_scouting():
    sheet_id = constants.SHEETS['scouting']['id']
    requests = [merge_cells(sheet_id, 1, 3, 0, 1), merge_cells(sheet_id, 0, 1, 2, 5), merge_cells(sheet_id, 0, 1, 5, 8)]
    
    return google_api.writeBatchUpdates(requests, constants.SPREADSHEET_ID)


def aesthetic_advanced_stats():
    sheet_id = constants.SHEETS['advanced_stats']['id']
    requests = []
    requests.append({
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": constants.TEAM_TOTAL + 1,
                    "startColumnIndex": 0,
                },
                "sortSpecs": [
                    {
                        "sortOrder": "DESCENDING",
                        "dimensionIndex": 2
                    }
                ]
            }
        }
    })
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 1,
                    "frozenColumnCount": 2,
                },
            },
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
        }
    })

    return google_api.writeBatchUpdates(requests, constants.SPREADSHEET_ID)


def aesthetic_ranking():
  sheet_id = constants.SHEETS['ranking']['id']
  requests = [merge_cells(sheet_id, 2, 6, 0, 1), merge_cells(sheet_id, 6, 6 + len(constants.COLS_W_OBSERVATIONS), 0, 1)]
  requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 2,
                    "frozenColumnCount": 2,
                },
            },
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
        }
  })
  requests.append({
      "setBasicFilter": {
          "filter": {
              "range": {
                  "sheetId": sheet_id,
                  "startRowIndex": 1,
                  "endRowIndex": constants.TEAM_TOTAL + 2,
                  "startColumnIndex": 0,
                  "endColumnIndex": 6 + len(constants.COLS_W_OBSERVATIONS) + 1
              },
              "sortSpecs": [
                  {
                      "sortOrder": "DESCENDING",
                      "dimensionIndex": 2
                  }
              ]
          }
      }
  })

  formula_col = num_to_A1(5 + len(constants.COLS_W_OBSERVATIONS) + 1)
  requests.append({
      "addConditionalFormatRule": {
          "rule": {
              "ranges": [
                  {
                      "sheetId": sheet_id,
                      "startRowIndex": 2,
                      "endRowIndex": constants.TEAM_TOTAL + 2,
                      "startColumnIndex": 0,
                      "endColumnIndex": 6 + len(constants.COLS_W_OBSERVATIONS) + 1 
                  }
              ],
              "booleanRule": {
                  "condition": {
                      "type": "CUSTOM_FORMULA",
                      "values": [{
                          "userEnteredValue": f"=${formula_col}3=FALSE"
                      }]
                  },
                  "format": {
                      "backgroundColorStyle": {
                          "rgbColor": {
                              "red": 0.6,
                              "green": 0.6,
                              "blue": 0.6
                          }
                      }
                  }
              }
          },
          "index": 0
      }
  })



  gradient_colors = {
      "minpoint": {
            "colorStyle": {
                "rgbColor": {
                    "red": 0.902,
                    "green": 0.486,
                    "blue": 0.451
                }
            },
            "type": "MIN"
        },
        "midpoint": {
            "colorStyle": {
                "rgbColor": {
                    "red": 0.714,
                    "green": 0.843,
                    "blue": 0.659
                }
            },
            "type": "PERCENTILE",
            "value": "50"
        },
        "maxpoint": {
            "colorStyle": {
                "rgbColor": {
                    "red": 0.341,
                    "green": 0.733,
                    "blue": 0.541
                }
            },
            "type": "MAX"
        }
  }
  inverse_gradient_colors = {
      "minpoint": {
            "colorStyle": {
                "rgbColor": {
                    "red": 0.341,
                    "green": 0.733,
                    "blue": 0.541
                }
            },
            "type": "MIN"
        },
        "midpoint": {
            "colorStyle": {
                "rgbColor": {
                    "red": 0.714,
                    "green": 0.843,
                    "blue": 0.659
                }
            },
            "type": "PERCENTILE",
            "value": "50"
        },
        "maxpoint": {
            "colorStyle": {
                "rgbColor": {
                    "red": 0.902,
                    "green": 0.486,
                    "blue": 0.451
                }
            },
            "type": "MAX"
        }
  }
  for i in range(2, 6 + len(constants.COLS_W_OBSERVATIONS)):
    ranges = [{
        "sheetId": sheet_id,
        "startRowIndex": 2,
        "endRowIndex": constants.TEAM_TOTAL + 2,
        "startColumnIndex": i,
        "endColumnIndex": i + 1
    }]
    requests.append({
        "addConditionalFormatRule": {
            "rule": {
                "ranges": ranges,
                "gradientRule": gradient_colors if i != 4 else inverse_gradient_colors
            },
            "index": 1
        }
    })

  return google_api.writeBatchUpdates(requests, constants.SPREADSHEET_ID)


def aesthetics_compare():
    sheet_id = constants.SHEETS['compare']['id']

    requests = []
    requests.append({
      "addChart": {
        "chart": {
          "spec": {
            "title": "Team Advanced Stats Comparison",
            "basicChart": {
              "chartType": "COLUMN",
              "legendPosition": "TOP_LEGEND",
              "axis": [
                {
                  "position": "BOTTOM_AXIS",
                  "title": "Advanced Stats"
                }
              ],
              "domains": [
                {
                  "domain": {
                    "sourceRange": {
                      "sources": [
                        {
                          "sheetId": sheet_id,
                          "startRowIndex": 1,
                          "endRowIndex": 6,
                          "startColumnIndex": 0,
                          "endColumnIndex": 1
                        }
                      ]
                    }
                  }
                }
              ],
              "series": [
                {
                  "series": {
                    "sourceRange": {
                      "sources": [
                        {
                          "sheetId": sheet_id,
                          "startRowIndex": 1,
                          "endRowIndex": 6,
                          "startColumnIndex": 1,
                          "endColumnIndex": 2
                        }
                      ]
                    }
                  },
                  "targetAxis": "LEFT_AXIS"
                },
                {
                  "series": {
                    "sourceRange": {
                      "sources": [
                        {
                          "sheetId": sheet_id,
                          "startRowIndex": 1,
                          "endRowIndex": 6,
                          "startColumnIndex": 2,
                          "endColumnIndex": 3
                        }
                      ]
                    }
                  },
                  "targetAxis": "LEFT_AXIS"
                },
                {
                  "series": {
                    "sourceRange": {
                      "sources": [
                        {
                          "sheetId": sheet_id,
                          "startRowIndex": 1,
                          "endRowIndex": 6,
                          "startColumnIndex": 3,
                          "endColumnIndex": 4
                        }
                      ]
                    }
                  },
                  "targetAxis": "LEFT_AXIS"
                }
              ],
              "headerCount": 1
            }
          },
          "position": {
            "overlayPosition": {
                "anchorCell": {
                    "sheetId": sheet_id,
                    "rowIndex": 0,
                    "columnIndex": 6
                }
            }
          }
        }
      }
    })

    return google_api.writeBatchUpdates(requests, constants.SPREADSHEET_ID)


'''
******************************************************************************************
Helper functions
******************************************************************************************
'''

def merge_cells(sheet_id, startColumn, endColumn, startRow, endRow):
    return{
        "mergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": startRow,
                "endRowIndex": endRow,
                "startColumnIndex": startColumn,
                "endColumnIndex": endColumn
            },
            "mergeType": 0
        }
    }

def num_to_A1(num):
    start_index = 0   #  it can start either at 0 or at 1
    letter = ''
    while num > 25 + start_index:   
        letter += chr(65 + int((num-start_index)/26) - 1)
        num = num - (int((num-start_index)/26))*26
    letter += chr(65 - start_index + (int(num)))
    return letter


if __name__ == "__main__":
    aesthetics_compare()