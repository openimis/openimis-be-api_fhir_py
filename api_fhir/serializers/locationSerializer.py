import copy

from location.models import HealthFacility

from api_fhir.converters.locationConverter import LocationConverter
from api_fhir.serializers import BaseFHIRSerializer


class LocationSerializer(BaseFHIRSerializer):
    fhirConverter = LocationConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return HealthFacility.objects.create(**copied_data)

    def update(self, instance, validated_data):
        # TODO add update statements
        instance.save()
        return instance