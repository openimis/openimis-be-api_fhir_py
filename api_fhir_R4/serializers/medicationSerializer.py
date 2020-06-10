import copy
from medical.models import Item
from api_fhir_R4.converters import MedicationConverter
from api_fhir_R4.serializers import BaseFHIRSerializer


class MedicationSerializer(BaseFHIRSerializer):
    fhirConverter = MedicationConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Item.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.package = validated_data.get('package', instance.package)
        instance.price = validated_data.get('price', instance.price)
        return instance
