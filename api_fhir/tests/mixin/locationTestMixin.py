from location.models import HealthFacility

from api_fhir.configurations import Stu3IdentifierConfig, Stu3LocationConfig
from api_fhir.converters import LocationConverter
from api_fhir.models import ContactPointSystem, AddressType, AddressUse, ContactPointUse, Location
from api_fhir.tests import GenericTestMixin


class LocationTestMixin(GenericTestMixin):

    _TEST_ID = 1
    _TEST_UUID = "6d0eea8c-62eb-11ea-94d6-c36229a16c2f"
    _TEST_HF_CODE = "12345678"
    _TEST_HF_NAME = "TEST_NAME"
    _TEST_HF_LEVEL = "H"
    _TEST_HF_LEGAL_FORM = "G"
    _TEST_ADDRESS = "TEST_ADDRESS"
    _TEST_PHONE = "133-996-476"
    _TEST_FAX = "1-408-999 8888"
    _TEST_EMAIL = "TEST@TEST.com"
    _TEST_LOCATION_ID = 1
    _TEST_LOCATION_UUID = "75250515-40d7-4c77-bafe-a2c65ffc5a72"

    def create_test_imis_instance(self):
        hf = HealthFacility()
        hf.id = self._TEST_ID
        hf.uuid = self._TEST_UUID
        hf.code = self._TEST_HF_CODE
        hf.name = self._TEST_HF_NAME
        hf.level = self._TEST_HF_LEVEL
        hf.legal_form_id = self._TEST_HF_LEGAL_FORM
        hf.address = self._TEST_ADDRESS
        hf.phone = self._TEST_PHONE
        hf.fax = self._TEST_FAX
        hf.email = self._TEST_EMAIL
        hf.location_id = self._TEST_LOCATION_ID
        return hf

    def verify_imis_instance(self, imis_obj):
        self.assertEqual(self._TEST_HF_CODE, imis_obj.code)
        self.assertEqual(self._TEST_HF_NAME, imis_obj.name)
        self.assertEqual(self._TEST_HF_LEVEL, imis_obj.level)
        # self.assertEqual(self._TEST_HF_LEGAL_FORM, imis_obj.legal_form)
        self.assertEqual(self._TEST_ADDRESS, imis_obj.address)
        self.assertEqual(self._TEST_PHONE, imis_obj.phone)
        self.assertEqual(self._TEST_FAX, imis_obj.fax)
        self.assertEqual(self._TEST_EMAIL, imis_obj.email)

    def create_test_fhir_instance(self):
        location = Location()
        identifier = LocationConverter.build_fhir_identifier(self._TEST_HF_CODE,
                                                             Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                             Stu3IdentifierConfig.get_fhir_facility_id_type())
        location.identifier = [identifier]
        location.name = self._TEST_HF_NAME
        location.type = LocationConverter.build_codeable_concept(
            Stu3LocationConfig.get_fhir_code_for_hospital(),
            Stu3LocationConfig.get_fhir_location_role_type_system())
        location.address = LocationConverter.build_fhir_address(self._TEST_ADDRESS, AddressUse.HOME.value,
                                                                AddressType.PHYSICAL.value)
        telecom = []
        phone = LocationConverter.build_fhir_contact_point(self._TEST_PHONE, ContactPointSystem.PHONE.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(phone)
        fax = LocationConverter.build_fhir_contact_point(self._TEST_FAX, ContactPointSystem.FAX.value,
                                                         ContactPointUse.HOME.value)
        telecom.append(fax)
        email = LocationConverter.build_fhir_contact_point(self._TEST_EMAIL, ContactPointSystem.EMAIL.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(email)
        location.telecom = telecom

        return location

    def verify_fhir_instance(self, fhir_obj):
        for identifier in fhir_obj.identifier:
            code = LocationConverter.get_first_coding_from_codeable_concept(identifier.type).code
            if code == Stu3IdentifierConfig.get_fhir_uuid_type_code():
                self.assertEqual(fhir_obj.id, identifier.value)
            elif code == Stu3IdentifierConfig.get_fhir_facility_id_type():
                self.assertEqual(self._TEST_HF_CODE, identifier.value)
        self.assertEqual(self._TEST_HF_NAME, fhir_obj.name)
        type_code = LocationConverter.get_first_coding_from_codeable_concept(fhir_obj.type).code
        self.assertEqual(Stu3LocationConfig.get_fhir_code_for_hospital(), type_code)
        self.assertEqual(self._TEST_ADDRESS, fhir_obj.address.text)
        self.assertEqual(3, len(fhir_obj.telecom))
        for telecom in fhir_obj.telecom:
            if telecom.system == ContactPointSystem.PHONE.value:
                self.assertEqual(self._TEST_PHONE, telecom.value)
            elif telecom.system == ContactPointSystem.EMAIL.value:
                self.assertEqual(self._TEST_EMAIL, telecom.value)
            elif telecom.system == ContactPointSystem.FAX.value:
                self.assertEqual(self._TEST_FAX, telecom.value)
