import copy

from claim.models import ClaimAdmin

from api_fhir.converters import PractitionerConverter
from api_fhir.exceptions import FHIRException
from api_fhir.serializers import BaseFHIRSerializer


class PractitionerSerializer(BaseFHIRSerializer):

    fhirConverter = PractitionerConverter()

    def create(self, validated_data):
        code = validated_data.get('code')
        if ClaimAdmin.objects.filter(code=code).count() > 0:
            raise FHIRException('Exists practitioner with following code `{}`'.format(code))
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return ClaimAdmin.objects.create(**copied_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.other_names = validated_data.get('other_names', instance.other_names)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email_id = validated_data.get('email_id', instance.email_id)
        instance.audit_user_id = self.get_audit_user_id()
        instance.save()
        return instance
