from claim.models import ClaimAdmin, Claim, Feedback
from insuree.models import Insuree
from location.models import HealthFacility

from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api_fhir.paginations import FhirBundleResultsSetPagination
from api_fhir.permissions import FHIRApiPermissions
from api_fhir.configurations import Stu3EligibilityConfiguration as Config
from api_fhir.serializers import PatientSerializer, LocationSerializer, PractitionerRoleSerializer, \
    PractitionerSerializer, ClaimSerializer, EligibilityRequestSerializer, PolicyEligibilityRequestSerializer, \
    ClaimResponseSerializer, CommunicationRequestSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class BaseFHIRView(APIView):
    pagination_class = FhirBundleResultsSetPagination
    permission_classes = (FHIRApiPermissions,)
    authentication_classes = [CsrfExemptSessionAuthentication] + APIView.settings.DEFAULT_AUTHENTICATION_CLASSES


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


class CommunicationRequestViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = CommunicationRequestSerializer


class EligibilityRequestViewSet(BaseFHIRView, mixins.CreateModelMixin, GenericViewSet):
    queryset = Insuree.objects.none()
    serializer_class = eval(Config.get_serializer())
