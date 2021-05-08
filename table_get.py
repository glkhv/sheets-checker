from pprint import pprint

import string
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from google_sheet_service import GoogleSheetService


service = GoogleSheetService().get_service()


def get_values(spreadsheet_id, cell):
    value = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = cell,
        majorDimension = 'ROWS'
    ).execute()
    return value.get('values')


res = get_values('1vbWr-v4WKx1sUzTTe1cp89A4qZOgj6CY2XIuF9Wst20', 'A1:Z1000')
pprint(res)
