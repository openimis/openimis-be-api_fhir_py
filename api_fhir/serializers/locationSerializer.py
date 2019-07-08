import copy

from location.models import HealthFacility

from api_fhir.converters import LocationConverter
from api_fhir.serializers import BaseFHIRSerializer


class LocationSerializer(BaseFHIRSerializer):
    fhirConverter = LocationConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return HealthFacility.objects.create(**copied_data)

    def update(self, instance, validated_data):
        # TODO legalForm isn't covered because that value is missing in the model
        # TODO LocationId isn't covered because that value is missing in the model
        # TODO offline isn't covered in the current version of API
        # TODO care_type isn't covered in the current version of API
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.level = validated_data.get('level', instance.level)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.fax = validated_data.get('fax', instance.fax)
        instance.email = validated_data.get('email', instance.email)
        instance.audit_user_id = self.get_audit_user_id()
        instance.save()
        return instance
