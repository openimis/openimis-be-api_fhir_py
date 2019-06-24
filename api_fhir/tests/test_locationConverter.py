import os

from django.test import TestCase
from location.models import HealthFacility

from api_fhir.configurations import Stu3IdentifierConfig, Stu3LocationConfig
from api_fhir.converters.locationConverter import LocationConverter
from api_fhir.models import ContactPointSystem, Location, ContactPointUse, FHIRBaseObject
from api_fhir.models.address import AddressUse, AddressType


class LocationConverterTestCase(TestCase):

    __TEST_ID = 1
    __TEST_HF_CODE = "12345678"
    __TEST_HF_NAME = "TEST_NAME"
    __TEST_HF_LEVEL = "H"
    __TEST_ADDRESS = "TEST_ADDRESS"
    __TEST_PHONE = "133-996-476"
    __TEST_FAX = "1-408-999 8888"
    __TEST_EMAIL = "TEST@TEST.com"
    __TEST_LOCATION_JSON_PATH = "/test/test_location.json"

    def __set_up(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_location_json_representation = open(dir_path + self.__TEST_LOCATION_JSON_PATH).read()

    def test_to_fhir_obj(self):
        imis_hf = self.__create_imis_health_facility_test_instance()
        fhir_location = LocationConverter.to_fhir_obj(imis_hf)
        self.verify_fhir_location(fhir_location)

    def test_to_imis_obj(self):
        fhir_loaction = self.__create_fhir_location_test_instance()
        imis_hf = LocationConverter.to_imis_obj(fhir_loaction, None)

        self.assertEqual(self.__TEST_HF_CODE, imis_hf.code)
        self.assertEqual(self.__TEST_HF_NAME, imis_hf.name)
        self.assertEqual(self.__TEST_HF_LEVEL, imis_hf.level)
        self.assertEqual(self.__TEST_ADDRESS, imis_hf.address)
        self.assertEqual(self.__TEST_PHONE, imis_hf.phone)
        self.assertEqual(self.__TEST_FAX, imis_hf.fax)
        self.assertEqual(self.__TEST_EMAIL, imis_hf.email)

    def test_create_object_from_json(self):
        self.__set_up()
        fhir_location = FHIRBaseObject.loads(self._test_location_json_representation, 'json')
        self.verify_fhir_location(fhir_location)

    def test_fhir_object_to_json(self):
        self.__set_up()
        fhir_location = self.__create_fhir_location_test_instance()
        location_id = LocationConverter.build_fhir_identifier(self.__TEST_ID,
                                                        Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                        Stu3IdentifierConfig.get_fhir_id_type_code())
        fhir_location.identifier.append(location_id)
        actual_representation = FHIRBaseObject.dumps(fhir_location, 'json')
        self.assertEqual(self._test_location_json_representation, actual_representation)

    def verify_fhir_location(self, fhir_location):
        self.assertEqual(2, len(fhir_location.identifier))
        for identifier in fhir_location.identifier:
            code = LocationConverter.get_first_coding_from_codeable_concept(identifier.type).code
            if code == Stu3IdentifierConfig.get_fhir_id_type_code():
                self.assertEqual(str(self.__TEST_ID), identifier.value)
            elif code == Stu3IdentifierConfig.get_fhir_facility_id_type():
                self.assertEqual(self.__TEST_HF_CODE, identifier.value)
        self.assertEqual(self.__TEST_HF_NAME, fhir_location.name)
        type_code = LocationConverter.get_first_coding_from_codeable_concept(fhir_location.type).code
        self.assertEqual(Stu3LocationConfig.get_fhir_code_for_hospital(), type_code)
        self.assertEqual(self.__TEST_ADDRESS, fhir_location.address.text)
        self.assertEqual(3, len(fhir_location.telecom))
        for telecom in fhir_location.telecom:
            if telecom.system == ContactPointSystem.PHONE.value:
                self.assertEqual(self.__TEST_PHONE, telecom.value)
            elif telecom.system == ContactPointSystem.EMAIL.value:
                self.assertEqual(self.__TEST_EMAIL, telecom.value)
            elif telecom.system == ContactPointSystem.FAX.value:
                self.assertEqual(self.__TEST_FAX, telecom.value)

    def __create_imis_health_facility_test_instance(self):
        hf = HealthFacility()
        hf.id = self.__TEST_ID
        hf.code = self.__TEST_HF_CODE
        hf.name = self.__TEST_HF_NAME
        hf.level = self.__TEST_HF_LEVEL
        hf.address = self.__TEST_ADDRESS
        hf.phone = self.__TEST_PHONE
        hf.fax = self.__TEST_FAX
        hf.email = self.__TEST_EMAIL
        return hf

    def __create_fhir_location_test_instance(self):
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
