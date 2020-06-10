import copy
from medical.models import Diagnosis
from api_fhir_R4.converters import ConditionConverter
from api_fhir_R4.serializers import BaseFHIRSerializer


class ConditionSerializer(BaseFHIRSerializer):
    fhirConverter = ConditionConverter

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Diagnosis.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.validity_from = validated_data.get('package', instance.validity_from)
        return instance
