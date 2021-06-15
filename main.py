import sys
from pprint import pprint
from google_sheet_service import GoogleSheetService
from value_comparison_service import ValueComparisonService
from charts_comparison_service import ChartsComparisonService
from link_service import get_sheet_id_from_link


system_score = 100
table_values_ratio = 0.6
charts_ratio = 0.4


if __name__ == "__main__":
    try:
        link_of_correct_doc = sys.argv[1]
        link_of_doc_to_check = sys.argv[2]

        sample_id = get_sheet_id_from_link(link_of_correct_doc)
        check_id = get_sheet_id_from_link(link_of_doc_to_check)

        service = GoogleSheetService().get_service()

        value_comparison = ValueComparisonService(service)
        value_compare_result = value_comparison.compare_values(sample_id, check_id)
        value_comparison_result = round(value_compare_result[0] / (value_compare_result[0] + len(value_compare_result[1])), 2)

        charts_comparison_service = ChartsComparisonService(service)
        charts_comparison_result = round(charts_comparison_service.compare(check_id, sample_id), 2)

        result = round(system_score * (table_values_ratio * value_comparison_result + charts_ratio * charts_comparison_result), 2)
        pprint(f"result: {result}")
    except:
        pprint("incorrect main func params")
