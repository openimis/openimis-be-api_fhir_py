from django.http.response import HttpResponseBase

from api_fhir.configurations import GeneralConfiguration
from rest_framework import serializers
from api_fhir.converters import BaseFHIRConverter, OperationOutcomeConverter
from api_fhir.models import FHIRBaseObject


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


from api_fhir.serializers.patientSerializer import PatientSerializer
from api_fhir.serializers.locationSerializer import LocationSerializer
from api_fhir.serializers.practitionerRoleSerializer import PractitionerRoleSerializer
from api_fhir.serializers.practitionerSerializer import PractitionerSerializer
from api_fhir.serializers.claimSerializer import ClaimSerializer
from api_fhir.serializers.eligibilityRequestSerializer import EligibilityRequestSerializer
from api_fhir.serializers.policyEligibilityRequestSerializer import PolicyEligibilityRequestSerializer
from api_fhir.serializers.claimResponseSerializer import ClaimResponseSerializer
from api_fhir.serializers.communicationRequestSerializer import CommunicationRequestSerializer
