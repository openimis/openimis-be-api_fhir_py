import copy
from medical.models import Service
from api_fhir_R4.converters import ActivityDefinitionConverter
from api_fhir_R4.serializers import BaseFHIRSerializer


class ActivityDefinitionSerializer(BaseFHIRSerializer):
    fhirConverter = ActivityDefinitionConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Service.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.validity_from = validated_data.get('validity_from', instance.validity_from)
        instance.patient_category = validated_data.get('patient_category', instance.patient_category)
        instance.category = validated_data.get('category', instance.category)
        instance.care_type = validated_data.get('care_type', instance.care_type)
        instance.type = validated_data.get('type', instance.type)
        instance.price = validated_data.get('price', instance.price)
        return instance
