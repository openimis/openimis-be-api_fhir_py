from api_fhir_R4.converters import OperationOutcomeConverter
from api_fhir_R4.permissions import FHIRApiClaimPermissions, FHIRApiCoverageEligibilityRequestPermissions, \
    FHIRApiCoverageRequestPermissions, FHIRApiCommunicationRequestPermissions, FHIRApiPractitionerPermissions, \
    FHIRApiHFPermissions, FHIRApiInsureePermissions, FHIRApiMedicationPermissions, FHIRApiConditionPermissions, \
    FHIRApiActivityDefinitionPermissions, FHIRApiHealthServicePermissions
from claim.models import ClaimAdmin, Claim, Feedback
from django.db.models import OuterRef, Exists
from insuree.models import Insuree
from location.models import HealthFacility, Location
from policy.models import Policy
from medical.models import Item, Diagnosis, Service

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
import datetime
from api_fhir_R4.paginations import FhirBundleResultsSetPagination
from api_fhir_R4.permissions import FHIRApiPermissions
from api_fhir_R4.configurations import R4CoverageEligibilityConfiguration as Config
from api_fhir_R4.serializers import PatientSerializer, LocationSerializer, PractitionerRoleSerializer, \
    PractitionerSerializer, ClaimSerializer, CoverageEligibilityRequestSerializer, \
    PolicyCoverageEligibilityRequestSerializer, ClaimResponseSerializer, CommunicationRequestSerializer, \
    MedicationSerializer, ConditionSerializer, ActivityDefinitionSerializer, HealthcareServiceSerializer
from api_fhir_R4.serializers.coverageSerializer import CoverageSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class BaseFHIRView(APIView):
    pagination_class = FhirBundleResultsSetPagination
    permission_classes = (FHIRApiPermissions,)
    authentication_classes = [CsrfExemptSessionAuthentication] + APIView.settings.DEFAULT_AUTHENTICATION_CLASSES


class InsureeViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = PatientSerializer
    permission_classes = (FHIRApiInsureePermissions,)

    def list(self, request, *args, **kwargs):
        claim_date = request.GET.get('claimDateFrom')
        identifier = request.GET.get("identifier")

        queryset = self.get_queryset()

        if claim_date is not None:
            day, month, year = claim_date.split('-')
            try:
                claim_date_parsed = datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                result = OperationOutcomeConverter.build_for_400_bad_request("claimDateFrom should be in dd-mm-yyyy format")
                return Response(result.toDict(), status.HTTP_400_BAD_REQUEST)
            has_claim_in_range = Claim.objects\
                .filter(date_claimed__gte=claim_date_parsed)\
                .filter(insuree_id=OuterRef("id"))\
                .values("id")
            queryset = queryset.annotate(has_claim_in_range=Exists(has_claim_in_range)).filter(has_claim_in_range=True)

        if identifier:
            queryset = queryset.filter(chf_id=identifier)

        serializer = PatientSerializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return Insuree.get_queryset(None, self.request.user)


class LocationViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = LocationSerializer
    permission_classes = (FHIRApiHFPermissions,)

    def list(self, request, *args, **kwargs):
        identifier = request.GET.get("identifier")
        queryset = self.get_queryset()
        if identifier:
            queryset = queryset.filter(code=identifier)

        serializer = LocationSerializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return Location.get_queryset(None, self.request.user)


class PractitionerRoleViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = PractitionerRoleSerializer
    permission_classes = (FHIRApiPractitionerPermissions,)

    def perform_destroy(self, instance):
        instance.health_facility_id = None
        instance.save()

    def get_queryset(self):
        return ClaimAdmin.get_queryset(None, self.request.user)


class PractitionerViewSet(BaseFHIRView, viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = PractitionerSerializer
    permission_classes = (FHIRApiPractitionerPermissions,)

    def list(self, request, *args, **kwargs):
        identifier = request.GET.get("identifier")
        queryset = self.get_queryset()
        if identifier:
            queryset = queryset.filter(code=identifier)

        serializer = PractitionerSerializer(self.paginate_queryset(queryset), many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return ClaimAdmin.get_queryset(None, self.request.user)


class ClaimViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = ClaimSerializer
    permission_classes = (FHIRApiClaimPermissions,)

    def get_queryset(self):
        return Claim.get_queryset(None, self.request.user)


class ClaimResponseViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = ClaimResponseSerializer
    permission_classes = (FHIRApiClaimPermissions,)

    def get_queryset(self):
        return Claim.get_queryset(None, self.request.user)


class CommunicationRequestViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = CommunicationRequestSerializer
    permission_classes = (FHIRApiCommunicationRequestPermissions,)

    def get_queryset(self):
        return Feedback.get_queryset(None, self.request.user)


class CoverageEligibilityRequestViewSet(BaseFHIRView, mixins.CreateModelMixin, GenericViewSet):
    queryset = Insuree.filter_queryset()
    serializer_class = eval(Config.get_serializer())
    #serializer_class = CoverageEligibilityRequestSerializer
    permission_classes = (FHIRApiCoverageEligibilityRequestPermissions,)

    def get_queryset(self):
        return Insuree.get_queryset(None, self.request.user)


class CoverageRequestQuerySet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = CoverageSerializer
    permission_classes = (FHIRApiCoverageRequestPermissions,)

    def get_queryset(self):
        return Policy.get_queryset(None, self.request.user)


class MedicationViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = MedicationSerializer
    permission_classes = (FHIRApiMedicationPermissions,)

    def get_queryset(self):
        return Item.get_queryset(None, self.request.user)


class ConditionViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'id'
    serializer_class = ConditionSerializer
    permission_classes = (FHIRApiConditionPermissions,)

    def get_queryset(self):
        return Diagnosis.get_queryset(None, self.request.user)


class ActivityDefinitionViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = ActivityDefinitionSerializer
    permission_classes = (FHIRApiActivityDefinitionPermissions,)

    def get_queryset(self):
        return Service.get_queryset(None, self.request.user)


class HealthcareServiceViewSet(BaseFHIRView, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    serializer_class = HealthcareServiceSerializer
    permission_classes = (FHIRApiHealthServicePermissions,)

    def get_queryset(self):
        return HealthFacility.get_queryset(None, self.request.user)
