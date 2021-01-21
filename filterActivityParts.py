import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrojanProject.settings')
django.setup()

from ActivitiesApp.models import ActivityPartModel
from PartsApp.models import PartSupplierModel

s = PartSupplierModel.objects.filter(supplier__supplierName__contains='TROJAN').values_list('part_id')
p = ActivityPartModel.objects.filter(increment=True, part_id__in=s)
p2 = ActivityPartModel.objects.filter(increment=False, part_id__in=s)
output = set()
for part in p:
    if part not in p2:
        output.add(part.part)

for part in p2:
    if part not in p:
        output.add(part.part)

for part in output:
    print(f'{part.id},{part.partNumber}')




