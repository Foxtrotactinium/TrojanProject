import csv
import os
import django
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrojanProject.settings')
django.setup()

from PartsApp.models import PartModel
from datetime import datetime

def export_stocktake_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocktake.csv"'

    writer = csv.writer(response)
    writer.writerow(['partNumber','description', 'location', 'stockOnHand'])

    target_date = datetime(2023, 6, 18)  # Specify the target date you want to query

    parts_dict = {}

    # Retrieve all historical records for PartModel
    historical_parts = PartModel.history.filter(history_date__lte=target_date)

    # Iterate over the historical records and track the latest entry for each partNumber
    for part in historical_parts:
        part_number = part.partNumber
        if part_number not in parts_dict or part.history_date > parts_dict[part_number].history_date:
            parts_dict[part_number] = part

    # Write the latest entries to the CSV file
    for part in parts_dict.values():
        part_data = [part.partNumber, part.description, part.location, part.stockOnHand]
        writer.writerow(part_data)

    return response