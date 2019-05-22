from insuree.models import Insuree

from rest_framework import viewsets

from api_fhir.serializers import PatientSerializer
from rest_framework_rules.mixins import PermissionRequiredMixin


class InsureeViewSet(viewsets.ModelViewSet):
    queryset = Insuree.objects.all()
    serializer_class = PatientSerializer
