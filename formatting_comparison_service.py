from google_sheet_service import GoogleSheetService
import requests

service = GoogleSheetService().get_service()

class FormattingComparisonService:

    def SendRequest(self, spreadsheet_id):
        address = 'https://sheets.googleapis.com/v4/spreadsheets/%s:batchGet()' % spreadsheet_id
        return requests.get(address)

    def GetData(self, spreadsheet_id):
        params = {
            'fields':'sheets(properties(title,sheetId),conditionalFormats)'}
        value = service.spreadsheets().values().get(
            spreadsheetId = spreadsheet_id,
            range = 'A1:Z1000',
            fields = params
        ).execute()
        return value