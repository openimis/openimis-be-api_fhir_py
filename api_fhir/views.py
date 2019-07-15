from claim.models import ClaimAdmin, Claim
from insuree.models import Insuree
from location.models import HealthFacility

from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from api_fhir.paginations import FhirBundleResultsSetPagination
from api_fhir.permissions import FHIRApiPermissions
from api_fhir.serializers import PatientSerializer, LocationSerializer, PractitionerRoleSerializer, \
    PractitionerSerializer, ClaimSerializer, EligibilityRequestSerializer, ClaimResponseSerializer


class BaseFHIRView(object):
    pagination_class = FhirBundleResultsSetPagination
    permission_classes = (FHIRApiPermissions,)


class InsureeViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = Insuree.objects.all()
    serializer_class = PatientSerializer


class HFViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = HealthFacility.objects.all()
    serializer_class = LocationSerializer


class PractitionerRoleViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerRoleSerializer

    def perform_destroy(self, instance):
        instance.health_facility_id = None
        instance.save()


class PractitionerViewSet(BaseFHIRView, viewsets.ModelViewSet):
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerSerializer


class ClaimViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    lookup_field = 'code'


class ClaimResponseViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimResponseSerializer
    lookup_field = 'code'


class EligibilityRequestViewSet(BaseFHIRView, mixins.CreateModelMixin, GenericViewSet):
    queryset = Insuree.objects.none()
    serializer_class = EligibilityRequestSerializer
