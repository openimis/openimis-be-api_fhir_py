from api_fhir.apiFhirConfiguration import ApiFhirConfiguration
from rest_framework import serializers
from api_fhir.converters import BaseFHIRConverter


class BaseFHIRSerializer(serializers.Serializer):
    fhirConverter = BaseFHIRConverter()

    def to_representation(self, obj):
        return self.fhirConverter.to_fhir_obj(obj).__dict__

    def to_internal_value(self, data):
        audit_user_id = self.getAuditUserId()
        return self.fhirConverter.to_imis_obj(data, audit_user_id).__dict__

    def create(self, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def getAuditUserId(self):
        request = self.context.get("request")
        audit_user_id = request.query_params.get('auditUserId', None)
        if audit_user_id is None:
            audit_user_id = ApiFhirConfiguration.get_default_audit_user_id()
        return audit_user_id


from api_fhir.serializers.patientSerializer import PatientSerializer
