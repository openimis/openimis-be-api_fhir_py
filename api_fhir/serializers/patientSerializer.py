import copy

from insuree.models import Insuree, Gender, Education, Profession

from api_fhir.converters import PatientConverter
from api_fhir.exceptions import FHIRException
from api_fhir.serializers import BaseFHIRSerializer


class PatientSerializer(BaseFHIRSerializer):
    fhirConverter = PatientConverter()

    def create(self, validated_data):
        chf_id = validated_data.get('chf_id')
        if Insuree.objects.filter(chf_id=chf_id).count() > 0:
            raise FHIRException('Exists patient with following chfid `{}`'.format(chf_id))
        copied_data = copy.deepcopy(validated_data)
        del copied_data['_state']
        return Insuree.objects.create(**copied_data)

    def update(self, instance, validated_data):
        # TODO the familyid isn't covered because that value is missing in the model
        # TODO the photoId isn't covered because that value is missing in the model
        # TODO the typeofid isn't covered because that value is missing in the model
        # TODO the head isn't covered in the current version of API
        # TODO the card_issued isn't covered in the current version of API
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
        instance.audit_user_id = self.get_audit_user_id()
        instance.save()
        return instance
