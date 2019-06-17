from django.test import TestCase
from location.models import HealthFacility

from api_fhir.apiFhirConfiguration import ApiFhirConfiguration
from api_fhir.converters.locationConverter import LocationConverter
from api_fhir.models import ContactPointSystem, Location, Address, ContactPointUse
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

    def test_to_fhir_obj(self):
        imis_hf = self.__create_imis_health_facility_test_instance()
        fhir_location = LocationConverter.to_fhir_obj(imis_hf)

        self.assertEqual(2, len(fhir_location.identifier))
        for identifier in fhir_location.identifier:
            if identifier.get("type").get("code") == ApiFhirConfiguration.get_fhir_id_type_code():
                self.assertEqual(imis_hf.id, identifier.get("value"))
            elif identifier.get("type").get("code") == ApiFhirConfiguration.get_fhir_facility_id_type():
                self.assertEqual(imis_hf.code, identifier.get("value"))
        self.assertEqual(imis_hf.name, fhir_location.name)
        self.assertEqual(ApiFhirConfiguration.get_fhir_code_for_hospital(), fhir_location.type.get('coding')[0]
                         .get('code'))
        self.assertEqual(imis_hf.address, fhir_location.address.get("text"))
        self.assertEqual(3, len(fhir_location.telecom))
        for telecom in fhir_location.telecom:
            if telecom.get("system") == ContactPointSystem.PHONE.value:
                self.assertEqual(imis_hf.phone, telecom.get("value"))
            elif telecom.get("system") == ContactPointSystem.EMAIL.value:
                self.assertEqual(imis_hf.email, telecom.get("value"))
            elif telecom.get("system") == ContactPointSystem.FAX.value:
                self.assertEqual(imis_hf.fax, telecom.get("value"))

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
        identifiers = [LocationConverter.build_fhir_identifier(self.__TEST_HF_CODE,
                                                               ApiFhirConfiguration.get_fhir_identifier_type_system(),
                                                               ApiFhirConfiguration.get_fhir_facility_id_type()).__dict__]
        location.identifier = identifiers
        location.name = self.__TEST_HF_NAME
        location.type = LocationConverter.build_codeable_concept(
            ApiFhirConfiguration.get_fhir_code_for_hospital(),
            ApiFhirConfiguration.get_fhir_location_role_type_system()).__dict__
        location.address = LocationConverter.build_fhir_address(self.__TEST_ADDRESS, AddressUse.HOME.value,
                                                       AddressType.PHYSICAL.value).__dict__
        telecom = []
        phone = LocationConverter.build_fhir_contact_point(self.__TEST_PHONE, ContactPointSystem.PHONE.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(phone.__dict__)
        fax = LocationConverter.build_fhir_contact_point(self.__TEST_FAX, ContactPointSystem.FAX.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(fax.__dict__)
        email = LocationConverter.build_fhir_contact_point(self.__TEST_EMAIL, ContactPointSystem.EMAIL.value,
                                                           ContactPointUse.HOME.value)
        telecom.append(email.__dict__)
        location.telecom = telecom

        return location.__dict__