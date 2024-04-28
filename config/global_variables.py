from django.contrib.auth.models import Group


MUDIR_GROUP = None
UNIVERSITY_STAFF_GROUP = None
try:
    MUDIR_GROUP = Group.objects.get(name="TTJ Mudiri")
except:
    pass

try:
    UNIVERSITY_STAFF_GROUP = Group.objects.get(name="Universitet xodimi")
except:
    pass
