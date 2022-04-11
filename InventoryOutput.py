import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrojanProject.settings')
django.setup()

from PartsApp.models import PartModel
from datetime import datetime
from ActivitiesApp.models import ActivityPartModel
from PartsApp.models import PartSupplierModel


inventory =
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['employee','IG', 'follower', 'email', 'website', 'DA', 'youtube_url', 'youtube_name', 'subscriber', 'type','country'])

    users = Library.objects.all().values_list('employee','IG', 'follower', 'email', 'website', 'DA', 'youtube_url', 'youtube_name', 'subscriber', 'type','country')
    for user in users:
        writer.writerow(user)

    return response

# s = PartSupplierModel.objects.filter(supplier__supplierName__contains='TROJAN').values_list('part_id')
# p = ActivityPartModel.objects.filter(increment=True, part_id__in=s)
# p2 = ActivityPartModel.objects.filter(increment=False, part_id__in=s)
# output = set()
# for part in p:
#     if part not in p2:
#         output.add(part.part)
#
# for part in p2:
#     if part not in p:
#         output.add(part.part)
#
# for part in output:
#     print(f'{part.id},{part.partNumber}')
#
#
#
#
