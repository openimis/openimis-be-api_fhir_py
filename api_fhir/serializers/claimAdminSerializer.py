import copy

from claim.models import ClaimAdmin

from api_fhir.converters import ClaimAdminConverter
from api_fhir.serializers import BaseFHIRSerializer


class ClaimAdminSerializer(BaseFHIRSerializer):

    fhirConverter = ClaimAdminConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return ClaimAdmin.objects.create(**copied_data)

    def update(self, instance, validated_data):
        pass  # TODO need to be implemented

    class Meta:
        app_label = 'api_fhir'
