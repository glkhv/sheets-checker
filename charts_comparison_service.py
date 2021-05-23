from google_sheet_service import GoogleSheetService
from cell_service import get_column_name_by_index
from pprint import pprint


service = GoogleSheetService().get_service()


def compare(spreadsheet_id, correct_spreadsheet_id):
    correct_charts = get_charts(correct_spreadsheet_id)
    charts_to_check = get_charts(spreadsheet_id)
    incorrect_charts = dict()

    for correct_chart in correct_charts:
        title = correct_chart.get("spec").get("title")
        chart_to_check = None

        for chart in charts_to_check:
            if chart.get("spec").get("title") == title:
                chart_to_check = chart

        if chart_to_check is not None:
            result = compare_by_values(correct_chart, chart_to_check)
            if len(result) != 0:
                incorrect_charts[title] = result
        else:
            incorrect_charts[title] = list()

    return incorrect_charts


def compare_by_values(correct_chart, chart_to_check):
    incorrect_cells = list()

    incorrect_cells += check_domain_cells(correct_chart, chart_to_check)

    return incorrect_cells


def check_domain_cells(correct_chart, chart_to_check):
    incorrect_cells = list()
    try:
        correct_source_indexes = correct_chart.get("spec").get("basicChart").get("domains")[0].get("domain").get("sourceRange").get("sources")[0]
        source_indexes_to_check = chart_to_check.get("spec").get("basicChart").get("domains")[0].get("domain").get("sourceRange").get("sources")[0]
    except:
        correct_source_indexes = correct_chart.get("spec").get("pieChart").get("domain").get("sourceRange").get("sources")[0]
        source_indexes_to_check = chart_to_check.get("spec").get("pieChart").get("domain").get("sourceRange").get("sources")[0]

    incorrect_cells += check_indexes(correct_source_indexes, source_indexes_to_check)

    return incorrect_cells


def check_indexes(indexes, correct_indexes):
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
        incorrect_indexes.append(f'{get_column_name_by_index(start_column_index)}{start_row_index}:{get_column_name_by_index(end_column_index)}{end_row_index}')

    return incorrect_indexes


def get_charts(spreadsheet_id):
    sheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute().get("sheets")
    charts = list()
    for sheet in sheets:
        sheet_charts = sheet.get("charts")
        if sheet_charts is not None:
            for chart in sheet_charts:
                charts.append(chart)
    return charts


# if __name__ == "__main__":
#     spreadsheet_id = "1UYNIcy6FNgUjgz-jWga7YbdWOTR5xnOfsN5UdOv7JYQ"
#     correct_spreadsheet_id = "1vbWr-v4WKx1sUzTTe1cp89A4qZOgj6CY2XIuF9Wst20"
#     result = compare(spreadsheet_id, correct_spreadsheet_id)
#     pprint(result)
