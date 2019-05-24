from rest_framework import serializers
from api_fhir.converters import BaseFHIRConverter


class BaseFHIRSerializer(serializers.Serializer):
    fhirConverter = BaseFHIRConverter()

    def to_representation(self, obj):
        return self.fhirConverter.to_fhir_obj(obj).__dict__

    def to_internal_value(self, data):
        user = self.getLoggedUser()
        return self.fhirConverter.to_imis_obj(data, user).__dict__

    def create(self, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def getLoggedUser(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user


from api_fhir.serializers.patientSerializer import PatientSerializer
