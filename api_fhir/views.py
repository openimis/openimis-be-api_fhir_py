from claim.models import ClaimAdmin, Claim, Feedback
from insuree.models import Insuree
from location.models import HealthFacility

from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
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
    lookup_field = 'uuid'
    queryset = Insuree.objects.all()
    serializer_class = PatientSerializer

    def list(self, request, *args, **kwargs):
        identifier = request.GET.get("identifier")
        queryset = Insuree.objects.filter(validity_to__isnull=True)
        if identifier:
            queryset = queryset.filter(chf_id=identifier)

        serializer = PatientSerializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)


class HFViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = HealthFacility.objects.all()
    serializer_class = LocationSerializer

    def list(self, request, *args, **kwargs):
        identifier = request.GET.get("identifier")
        queryset = HealthFacility.objects.filter(validity_to__isnull=True)
        if identifier:
            queryset = queryset.filter(code=identifier)

        serializer = LocationSerializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)


class PractitionerRoleViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerRoleSerializer

    def perform_destroy(self, instance):
        instance.health_facility_id = None
        instance.save()


class PractitionerViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = ClaimAdmin.objects.all()
    serializer_class = PractitionerSerializer


class ClaimViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class ClaimResponseViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    queryset = Claim.objects.all()
    serializer_class = ClaimResponseSerializer


class CommunicationRequestViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    queryset = Feedback.objects.all()
    serializer_class = CommunicationRequestSerializer


class EligibilityRequestViewSet(BaseFHIRView, mixins.CreateModelMixin, GenericViewSet):
    queryset = Insuree.objects.none()
    serializer_class = eval(Config.get_serializer())
