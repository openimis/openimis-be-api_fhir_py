from rest_framework import serializers


class BaseFHIRConverter(object):
    @classmethod
    def toFhirObj(cls, obj):
        raise NotImplementedError('`toFhirObj()` must be implemented.')

    @classmethod
    def toImisObj(cls, data):
        raise NotImplementedError('`toImisObj()` must be implemented.')


class BaseFHIRSerializer(serializers.Serializer):
    fhirConverter = BaseFHIRConverter()

    def to_representation(self, obj):
        return self.fhirConverter.toFhirObj(obj).__dict__

    def to_internal_value(self, data):
        return self.fhirConverter.toImisObj(data).__dict__

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


from api_fhir.serializers.patientSerializer import PatientSerializer
