import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetService:

    CREDENTIALS_FILE = 'creds.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])

    def __init__(self):
        http_auth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    def get_service(self):
        return self.service
