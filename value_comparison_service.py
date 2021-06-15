check_range = 'A1:Z1000'
num_to_letter = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G',
                 '8': 'H', '9': 'I', '10': 'J', '11': 'K', '12': 'L', '13': 'M', '14': 'N',
                 '15': 'O', '16': 'P', '17': 'Q', '18': 'R', '19': 'S', '20': 'T', '21': 'U',
                 '22': 'V', '23': 'W', '24': 'X', '25': 'Y', '26': 'Z'}


class ValueComparisonService:

    def __init__(self, service):
        self.service = service

    def get_values(self, spreadsheet_id):
        try:
            value = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=check_range,
                majorDimension='ROWS'
            ).execute()
            return value.get('values')
        except:
            print('Lost connection (getting values)')
            return None

    def coordinates_to_cell(self, row, column):
        row = str(row + 1)
        column = num_to_letter.get(str(column + 1))
        return column + row

    def compare_values(self, spreadsheet_sample_id, spreadsheet_check_id):
        sample_values = self.get_values(spreadsheet_sample_id)
        check_values = self.get_values(spreadsheet_check_id)
        correct_counter = 0
        incorrect_answers = []

        try:
            for i in range(len(sample_values)):
                for j in range(len(sample_values[i])):
                    if check_values[i][j] == sample_values[i][j] and sample_values[i][j] != '':
                        correct_counter += 1
                    else:
                        incorrect_answers.append(self.coordinates_to_cell(i, j))
        except:
            correct_counter = 0
            print('Index out of range: Incorrect size of table')

        return correct_counter, incorrect_answers
