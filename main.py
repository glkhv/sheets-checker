from pprint import pprint

from google_sheet_service import GoogleSheetService
from value_comparison_service import ValueComparisonService


service = GoogleSheetService().get_service()

sample_id = '1vbWr-v4WKx1sUzTTe1cp89A4qZOgj6CY2XIuF9Wst20'
check_id = '1v9wokj-glQmqIJUkB9jQ8CaO-kWw_lfR0IX3EZHSptQ'

value_comparison = ValueComparisonService()
print(value_comparison.CompareValues(sample_id, check_id))
