from claim.models import ClaimAdmin, Claim
from insuree.models import Insuree
from location.models import HealthFacility

from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from api_fhir.serializers import PatientSerializer, LocationSerializer, PractitionerRoleSerializer, \
    PractitionerSerializer, ClaimSerializer


class InsureeViewSet(viewsets.ModelViewSet):
    queryset = Insuree.objects.all()
    serializer_class = PatientSerializer


class HFViewSet(viewsets.ModelViewSet):
    queryset = HealthFacility.objects.all()
    serializer_class = LocationSerializer


class PractitionerRoleViewSet(viewsets.ModelViewSet):
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerRoleSerializer

    def perform_destroy(self, instance):
        instance.health_facility_id = None
        instance.save()


class PractitionerViewSet(viewsets.ModelViewSet):
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerSerializer


class ClaimViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    lookup_field = 'code'
