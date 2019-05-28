from django.test import TestCase
from insuree.models import Insuree, Gender

from api_fhir.apiFhirConfiguration import ApiFhirConfiguration
from api_fhir.converters import PatientConverter
import core

from api_fhir.models import NameUse, AdministrativeGender, ImisMaritialStatus, ContactPointSystem, Patient, HumanName, \
    ContactPointUse
from api_fhir.models.address import AddressType, AddressUse


class PatientConverterTestCase(TestCase):

    __TEST_LAST_NAME = "TEST_LAST_NAME"
    __TEST_OTHER_NAME = "TEST_OTHER_NAME"
    __TEST_DOB = "1990-03-24"
    __TEST_ID = 1
    __TEST_CHF_ID = "TEST_CHF_ID"
    __TEST_PASSPORT = "TEST_PASSPORT"
    __TEST_GENDER_CODE = "M"
    __TEST_GENDER = None
    __TEST_PHONE = "813-996-476"
    __TEST_EMAIL = "TEST@TEST.com"
    __TEST_ADDRESS = "TEST_ADDRESS"
    __TEST_GEOLOCATION = "TEST_GEOLOCATION"

    def __set_up(self):
        self.__TEST_GENDER = Gender()
        self.__TEST_GENDER.code = self.__TEST_GENDER_CODE
        self.__TEST_GENDER.save()

    def test_to_fhir_obj(self):
        self.__set_up()
        imis_insuree = self.__create_imis_insuree_test_instance()
        fhir_patient = PatientConverter.to_fhir_obj(imis_insuree)

        self.assertEqual(1, len(fhir_patient.name))
        humanName = fhir_patient.name[0]
        self.assertEqual(imis_insuree.other_names, humanName.get("given")[0])
        self.assertEqual(imis_insuree.last_name, humanName.get("family"))
        self.assertEqual(imis_insuree.last_name, humanName.get("family"))
        self.assertEqual(NameUse.USUAL.value, humanName.get("use"))

        self.assertEqual(3, len(fhir_patient.identifier))
        for identifier in fhir_patient.identifier:
            if identifier.get("type").get("code") == ApiFhirConfiguration.get_fhir_chfid_type_code():
                self.assertEqual(imis_insuree.chf_id, identifier.get("value"))
            elif identifier.get("type").get("code") == ApiFhirConfiguration.get_fhir_id_type_code():
                self.assertEqual(imis_insuree.id, identifier.get("value"))
            elif identifier.get("type").get("code") == ApiFhirConfiguration.get_fhir_passport_type_code():
                self.assertEqual(imis_insuree.passport, identifier.get("value"))

        self.assertEqual(imis_insuree.dob.isoformat(), fhir_patient.birthDate)

        self.assertEqual(AdministrativeGender.MALE.value, fhir_patient.gender)

        self.assertEqual(ApiFhirConfiguration.get_fhir_divorced_code(), fhir_patient.maritalStatus.get("code"))

        self.assertEqual(2, len(fhir_patient.telecom))
        for telecom in fhir_patient.telecom:
            if telecom.get("system") == ContactPointSystem.PHONE.value:
                self.assertEqual(imis_insuree.phone, telecom.get("value"))
            elif telecom.get("system") == ContactPointSystem.EMAIL.value:
                self.assertEqual(imis_insuree.email, telecom.get("value"))

        self.assertEqual(2, len(fhir_patient.address))
        for adddress in fhir_patient.address:
            if adddress.get("type") == AddressType.PHYSICAL.value:
                self.assertEqual(imis_insuree.current_address, adddress.get("text"))
            elif adddress.get("type") == AddressType.BOTH.value:
                self.assertEqual(imis_insuree.geolocation, adddress.get("text"))

    def test_to_imis_obj(self):
        self.__set_up()
        fhir_patient = self.__create_fhir_patient_test_instance()
        imis_insuree = PatientConverter.to_imis_obj(fhir_patient, None)

        self.assertEqual(self.__TEST_LAST_NAME, imis_insuree.last_name)
        self.assertEqual(self.__TEST_OTHER_NAME, imis_insuree.other_names)

        self.assertEqual(self.__TEST_CHF_ID, imis_insuree.chf_id)
        self.assertEqual(self.__TEST_PASSPORT, imis_insuree.passport)
        self.assertEqual(self.__TEST_PASSPORT, imis_insuree.passport)
        expected_date = core.datetime.datetime.strptime(self.__TEST_DOB,
                                                           ApiFhirConfiguration.get_iso_date_format())
        self.assertEqual(expected_date, imis_insuree.dob)
        self.assertEqual(self.__TEST_GENDER_CODE, imis_insuree.gender.code)
        self.assertEqual(ImisMaritialStatus.DIVORCED.value, imis_insuree.marital)
        self.assertEqual(self.__TEST_PHONE, imis_insuree.phone)
        self.assertEqual(self.__TEST_EMAIL, imis_insuree.email)
        self.assertEqual(self.__TEST_ADDRESS, imis_insuree.current_address)
        self.assertEqual(self.__TEST_GEOLOCATION, imis_insuree.geolocation)


    def __create_imis_insuree_test_instance(self):
        imis_insuree = Insuree()
        imis_insuree.last_name = self.__TEST_LAST_NAME
        imis_insuree.other_names = self.__TEST_OTHER_NAME
        imis_insuree.id = self.__TEST_ID
        imis_insuree.chf_id = self.__TEST_CHF_ID
        imis_insuree.passport = self.__TEST_PASSPORT
        imis_insuree.dob = core.datetime.datetime.strptime(self.__TEST_DOB,
                                                           ApiFhirConfiguration.get_iso_date_format())
        imis_insuree.gender = self.__TEST_GENDER
        imis_insuree.marital = ImisMaritialStatus.DIVORCED.value
        imis_insuree.phone = self.__TEST_PHONE
        imis_insuree.email = self.__TEST_EMAIL
        imis_insuree.current_address = self.__TEST_ADDRESS
        imis_insuree.geolocation = self.__TEST_GEOLOCATION
        return imis_insuree

    def __create_fhir_patient_test_instance(self):
        fhir_patient = Patient()
        name = HumanName()
        name.family = self.__TEST_LAST_NAME
        name.given = [self.__TEST_OTHER_NAME]
        name.use = NameUse.USUAL.value
        fhir_patient.name = [name.__dict__]
        identifiers = []
        chf_id = PatientConverter.build_fhir_identifier(self.__TEST_CHF_ID,
                                                        ApiFhirConfiguration.get_fhir_identifier_type_system(),
                                                        ApiFhirConfiguration.get_fhir_chfid_type_code())
        identifiers.append(chf_id.__dict__)
        passport = PatientConverter.build_fhir_identifier(self.__TEST_PASSPORT,
                                               ApiFhirConfiguration.get_fhir_identifier_type_system(),
                                               ApiFhirConfiguration.get_fhir_passport_type_code())
        identifiers.append(passport.__dict__)
        fhir_patient.identifier = identifiers
        fhir_patient.birthDate = self.__TEST_DOB
        fhir_patient.gender = AdministrativeGender.MALE.value
        fhir_patient.maritalStatus = PatientConverter.build_codeable_concept(
            ApiFhirConfiguration.get_fhir_divorced_code(),
            ApiFhirConfiguration.get_fhir_marital_status_system()).__dict__
        telecom = []
        phone = PatientConverter.build_fhir_contact_point(self.__TEST_PHONE, ContactPointSystem.PHONE.value,
                                                          ContactPointUse.HOME.value)
        telecom.append(phone.__dict__)
        email = PatientConverter.build_fhir_contact_point(self.__TEST_EMAIL, ContactPointSystem.EMAIL.value,
                                                          ContactPointUse.HOME.value)
        telecom.append(email.__dict__)
        fhir_patient.telecom = telecom
        addresses = []
        current_address = PatientConverter.build_fhir_address(self.__TEST_ADDRESS, AddressUse.HOME.value,
                                                              AddressType.PHYSICAL.value)
        addresses.append(current_address.__dict__)
        geolocation = PatientConverter.build_fhir_address(self.__TEST_GEOLOCATION, AddressUse.HOME.value,
                                                          AddressType.BOTH.value)
        addresses.append(geolocation.__dict__)
        fhir_patient.address = addresses
        return fhir_patient.__dict__
