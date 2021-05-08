from pprint import pprint

import string
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
# spreadsheets_sample_id = input()
# spreadsheets_check_id = input()

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

#cells (columns and rows indexes)
columns_list = list(string.ascii_uppercase)
rows_list = list(range(1, 1001))

def GetValues(spreadsheet_id, cell):
    value = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = cell,
        majorDimension = 'ROWS'
    ).execute()
    return value.get('values')[0][0]

res = GetValues('1vbWr-v4WKx1sUzTTe1cp89A4qZOgj6CY2XIuF9Wst20', 'A1')
pprint(res)