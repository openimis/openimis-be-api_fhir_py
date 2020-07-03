from django.http.response import HttpResponseBase

from api_fhir_R4.configurations import GeneralConfiguration
from rest_framework import serializers
from api_fhir_R4.converters import BaseFHIRConverter, OperationOutcomeConverter
from api_fhir_R4.models import FHIRBaseObject


class BaseFHIRSerializer(serializers.Serializer):
    fhirConverter = BaseFHIRConverter()

    def to_representation(self, obj):
        if isinstance(obj, HttpResponseBase):
            return OperationOutcomeConverter.to_fhir_obj(obj).toDict()
        elif isinstance(obj, FHIRBaseObject):
            return obj.toDict()
        return self.fhirConverter.to_fhir_obj(obj).toDict()

    def to_internal_value(self, data):
        audit_user_id = self.get_audit_user_id()
        if isinstance(data, dict):
            data = FHIRBaseObject.fromDict(data)
        return self.fhirConverter.to_imis_obj(data, audit_user_id).__dict__

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')  # pragma: no cover

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')  # pragma: no cover

    def get_audit_user_id(self):
        request = self.context.get("request")
        # Taking the audit_user_id from the query doesn't seem wise but there might be a use for it
        # audit_user_id = request.query_params.get('auditUserId', None)
        audit_user_id = request.user.id_for_audit if request.user else None
        if audit_user_id is None:
            audit_user_id = GeneralConfiguration.get_default_audit_user_id()
        return audit_user_id


from api_fhir_R4.serializers.patientSerializer import PatientSerializer
from api_fhir_R4.serializers.locationSerializer import LocationSerializer
from api_fhir_R4.serializers.practitionerRoleSerializer import PractitionerRoleSerializer
from api_fhir_R4.serializers.practitionerSerializer import PractitionerSerializer
from api_fhir_R4.serializers.claimSerializer import ClaimSerializer
from api_fhir_R4.serializers.coverageEligibilityRequestSerializer import CoverageEligibilityRequestSerializer
from api_fhir_R4.serializers.policyCoverageEligibilityRequestSerializer import PolicyCoverageEligibilityRequestSerializer
from api_fhir_R4.serializers.claimResponseSerializer import ClaimResponseSerializer
from api_fhir_R4.serializers.communicationRequestSerializer import CommunicationRequestSerializer
from api_fhir_R4.serializers.medicationSerializer import MedicationSerializer
from api_fhir_R4.serializers.conditionSerializer import ConditionSerializer
from api_fhir_R4.serializers.activityDefinitionSerializer import ActivityDefinitionSerializer
from api_fhir_R4.serializers.healthcareServiceSerializer import HealthcareServiceSerializer
