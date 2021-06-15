from cell_service import get_column_name_by_index


class ChartsComparisonService:

    def __init__(self, service):
        self.service = service

    def compare(self, spreadsheet_id, correct_spreadsheet_id):
        correct_charts = self.get_charts(correct_spreadsheet_id)
        charts_to_check = self.get_charts(spreadsheet_id)
        incorrect_charts = dict()

        for correct_chart in correct_charts:
            title = correct_chart.get("spec").get("title")
            chart_to_check = None

            for chart in charts_to_check:
                if chart.get("spec").get("title") == title:
                    chart_to_check = chart

            if chart_to_check is not None:
                result = self.compare_by_values(correct_chart, chart_to_check)
                if len(result) != 0:
                    incorrect_charts[title] = result
            else:
                incorrect_charts[title] = list()

        ratio_of_one_chart = 1 / len(correct_charts)
        ratio_of_mistakes = ratio_of_one_chart * len(incorrect_charts)

        for key, value in incorrect_charts.items():
            if len(value) != 0:
                ratio_of_mistakes -= ratio_of_one_chart * 0.2

        return 1 - ratio_of_mistakes

    def compare_by_values(self, correct_chart, chart_to_check):
        incorrect_cells = list()

        incorrect_cells += self.check_domain_cells(correct_chart, chart_to_check)

        return incorrect_cells

    def check_domain_cells(self, correct_chart, chart_to_check):
        incorrect_cells = list()
        try:
            correct_source_indexes = \
                correct_chart.get("spec").get("basicChart").get("domains")[0].get("domain").get("sourceRange").get(
                    "sources")[0]
            source_indexes_to_check = \
                chart_to_check.get("spec").get("basicChart").get("domains")[0].get("domain").get("sourceRange").get(
                    "sources")[0]
        except:
            correct_source_indexes = \
                correct_chart.get("spec").get("pieChart").get("domain").get("sourceRange").get("sources")[0]
            source_indexes_to_check = \
                chart_to_check.get("spec").get("pieChart").get("domain").get("sourceRange").get("sources")[0]

        incorrect_cells += self.check_indexes(correct_source_indexes, source_indexes_to_check)

        return incorrect_cells

    def check_indexes(self, indexes, correct_indexes):
        incorrect_indexes = list()

        # Correct indexes
        correct_start_row_index = correct_indexes.get("startRowIndex")
        correct_start_column_index = correct_indexes.get("startColumnIndex")
        correct_end_row_index = correct_indexes.get("endRowIndex")
        correct_end_column_index = correct_indexes.get("endColumnIndex")

        # Indexes to check
        start_row_index = indexes.get("startRowIndex")
        start_column_index = indexes.get("startColumnIndex")
        end_row_index = indexes.get("endRowIndex")
        end_column_index = indexes.get("endColumnIndex")

        if correct_start_row_index != start_row_index or correct_start_column_index != start_column_index \
                or correct_end_row_index != end_row_index or correct_end_column_index != end_column_index:
            incorrect_indexes.append(
                f'{get_column_name_by_index(start_column_index)}{start_row_index}:{get_column_name_by_index(end_column_index)}{end_row_index}')

        return incorrect_indexes

    def get_charts(self, spreadsheet_id):
        sheets = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute().get("sheets")
        charts = list()
        for sheet in sheets:
            sheet_charts = sheet.get("charts")
            if sheet_charts is not None:
                for chart in sheet_charts:
                    charts.append(chart)
        return charts
