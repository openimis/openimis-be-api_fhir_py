from location.models import HealthFacility

from api_fhir.configurations import Stu3IdentifierConfig, Stu3LocationConfig
from api_fhir.converters import LocationConverter
from api_fhir.models import ContactPointSystem, AddressType, AddressUse, ContactPointUse, Location
from mixin.dbIdTestMixins import DbIdTestMixins
from mixin.genericTestMixin import GenericTestMixin


class LocationTestMixin(GenericTestMixin, DbIdTestMixins):

    __TEST_ID = 1
    __TEST_HF_CODE = "12345678"
    __TEST_HF_NAME = "TEST_NAME"
    __TEST_HF_LEVEL = "H"
    __TEST_ADDRESS = "TEST_ADDRESS"
    __TEST_PHONE = "133-996-476"
    __TEST_FAX = "1-408-999 8888"
    __TEST_EMAIL = "TEST@TEST.com"

    def get_test_db_id(self):
        return self.__TEST_ID

    def create_test_imis_instance(self):
        hf = HealthFacility()
        hf.id = self.get_test_db_id()
        hf.code = self.__TEST_HF_CODE
        hf.name = self.__TEST_HF_NAME
        hf.level = self.__TEST_HF_LEVEL
        hf.address = self.__TEST_ADDRESS
        hf.phone = self.__TEST_PHONE
        hf.fax = self.__TEST_FAX
        hf.email = self.__TEST_EMAIL
        return hf

    def verify_imis_instance(self, imis_obj):
        self.assertEqual(self.__TEST_HF_CODE, imis_obj.code)
        self.assertEqual(self.__TEST_HF_NAME, imis_obj.name)
        self.assertEqual(self.__TEST_HF_LEVEL, imis_obj.level)
        self.assertEqual(self.__TEST_ADDRESS, imis_obj.address)
        self.assertEqual(self.__TEST_PHONE, imis_obj.phone)
        self.assertEqual(self.__TEST_FAX, imis_obj.fax)
        self.assertEqual(self.__TEST_EMAIL, imis_obj.email)

    def create_test_fhir_instance(self):
        location = Location()
        identifier = LocationConverter.build_fhir_identifier(self.__TEST_HF_CODE,
                                                             Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                             Stu3IdentifierConfig.get_fhir_facility_id_type())
        location.identifier = [identifier]
        location.name = self.__TEST_HF_NAME
        location.type = LocationConverter.build_codeable_concept(
            Stu3LocationConfig.get_fhir_code_for_hospital(),
            Stu3LocationConfig.get_fhir_location_role_type_system())
        location.address = LocationConverter.build_fhir_address(self.__TEST_ADDRESS, AddressUse.HOME.value,
                                                                AddressType.PHYSICAL.value)
        telecom = []
        phone = LocationConverter.build_fhir_contact_point(self.__TEST_PHONE, ContactPointSystem.PHONE.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(phone)
        fax = LocationConverter.build_fhir_contact_point(self.__TEST_FAX, ContactPointSystem.FAX.value,
                                                         ContactPointUse.HOME.value)
        telecom.append(fax)
        email = LocationConverter.build_fhir_contact_point(self.__TEST_EMAIL, ContactPointSystem.EMAIL.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(email)
        location.telecom = telecom

        return location

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(2, len(fhir_obj.identifier))
        for identifier in fhir_obj.identifier:
            code = LocationConverter.get_first_coding_from_codeable_concept(identifier.type).code
            if code == Stu3IdentifierConfig.get_fhir_id_type_code():
                self.assertEqual(str(self.get_test_db_id()), identifier.value)
            elif code == Stu3IdentifierConfig.get_fhir_facility_id_type():
                self.assertEqual(self.__TEST_HF_CODE, identifier.value)
        self.assertEqual(self.__TEST_HF_NAME, fhir_obj.name)
        type_code = LocationConverter.get_first_coding_from_codeable_concept(fhir_obj.type).code
        self.assertEqual(Stu3LocationConfig.get_fhir_code_for_hospital(), type_code)
        self.assertEqual(self.__TEST_ADDRESS, fhir_obj.address.text)
        self.assertEqual(3, len(fhir_obj.telecom))
        for telecom in fhir_obj.telecom:
            if telecom.system == ContactPointSystem.PHONE.value:
                self.assertEqual(self.__TEST_PHONE, telecom.value)
            elif telecom.system == ContactPointSystem.EMAIL.value:
                self.assertEqual(self.__TEST_EMAIL, telecom.value)
            elif telecom.system == ContactPointSystem.FAX.value:
                self.assertEqual(self.__TEST_FAX, telecom.value)