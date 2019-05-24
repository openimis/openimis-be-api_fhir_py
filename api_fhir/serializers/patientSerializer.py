import copy

from insuree.models import Insuree, Gender
from rest_framework.exceptions import NotAuthenticated

from api_fhir.converters import PatientConverter
from api_fhir.serializers import BaseFHIRSerializer


class PatientSerializer(BaseFHIRSerializer):
    fhirConverter = PatientConverter()

    def create(self, validated_data):
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Insuree.objects.create(**copied_data)

    def update(self, instance, validated_data):
        # TODO the familyid isn't covered because that value is missing in the model
        # TODO the photoId isn't covered because that value is missing in the model
        # TODO the typeofid isn't covered because that value is missing in the model
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.other_names = validated_data.get('other_names', instance.other_names)
        instance.chf_id = validated_data.get('chf_id', instance.chf_id)
        instance.passport = validated_data.get('passport', instance.passport)
        instance.dob = validated_data.get('dob', instance.dob)
        gender_code = validated_data.get('gender_id', instance.gender.code)
        instance.gender = Gender.objects.get(pk=gender_code)
        instance.marital = validated_data.get('marital', instance.marital)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.current_address = validated_data.get('current_address', instance.current_address)
        instance.geolocation = validated_data.get('geolocation', instance.geolocation)

        current_user = self.getLoggedUser()
        if current_user is not None:
            instance.audit_user_id = 1 # TODO the audit_user_id isn't covered because current_user.id currently is of UUID type not an integer
        else:
            raise NotAuthenticated

        instance.save()
        return instance

    class Meta:
        app_label = 'api_fhir'
