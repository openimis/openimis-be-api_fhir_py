from insuree.models import Gender, Insuree

from api_fhir.configurations import Stu3IdentifierConfig, Stu3MaritalConfig
from api_fhir.converters import PatientConverter
from api_fhir.models import HumanName, NameUse, Identifier, AdministrativeGender, ContactPoint, ContactPointSystem, \
    Address, AddressType, ImisMaritalStatus, Patient, ContactPointUse, AddressUse
from api_fhir.tests import GenericTestMixin, DbIdTestMixin
from api_fhir.utils import TimeUtils


class PatientTestMixin(GenericTestMixin, DbIdTestMixin):

    __TEST_LAST_NAME = "TEST_LAST_NAME"
    __TEST_OTHER_NAME = "TEST_OTHER_NAME"
    __TEST_DOB = "1990-03-24T00:00:00"
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

    def get_test_db_id(self):
        return self.__TEST_ID

    def create_test_imis_instance(self):
        self.__set_up()
        imis_insuree = Insuree()
        imis_insuree.last_name = self.__TEST_LAST_NAME
        imis_insuree.other_names = self.__TEST_OTHER_NAME
        imis_insuree.id = self.get_test_db_id()
        imis_insuree.chf_id = self.__TEST_CHF_ID
        imis_insuree.passport = self.__TEST_PASSPORT
        imis_insuree.dob = TimeUtils.str_to_date(self.__TEST_DOB)
        imis_insuree.gender = self.__TEST_GENDER
        imis_insuree.marital = ImisMaritalStatus.DIVORCED.value
        imis_insuree.phone = self.__TEST_PHONE
        imis_insuree.email = self.__TEST_EMAIL
        imis_insuree.current_address = self.__TEST_ADDRESS
        imis_insuree.geolocation = self.__TEST_GEOLOCATION
        return imis_insuree

    def verify_imis_instance(self, imis_obj):
        self.assertEqual(self.__TEST_LAST_NAME, imis_obj.last_name)
        self.assertEqual(self.__TEST_OTHER_NAME, imis_obj.other_names)
        self.assertEqual(self.__TEST_CHF_ID, imis_obj.chf_id)
        self.assertEqual(self.__TEST_PASSPORT, imis_obj.passport)
        expected_date = TimeUtils.str_to_date(self.__TEST_DOB)
        self.assertEqual(expected_date, imis_obj.dob)
        self.assertEqual(self.__TEST_GENDER_CODE, imis_obj.gender.code)
        self.assertEqual(ImisMaritalStatus.DIVORCED.value, imis_obj.marital)
        self.assertEqual(self.__TEST_PHONE, imis_obj.phone)
        self.assertEqual(self.__TEST_EMAIL, imis_obj.email)
        self.assertEqual(self.__TEST_ADDRESS, imis_obj.current_address)
        self.assertEqual(self.__TEST_GEOLOCATION, imis_obj.geolocation)

    def create_test_fhir_instance(self):
        self.__set_up()
        fhir_patient = Patient()
        name = HumanName()
        name.family = self.__TEST_LAST_NAME
        name.given = [self.__TEST_OTHER_NAME]
        name.use = NameUse.USUAL.value
        fhir_patient.name = [name]
        identifiers = []
        chf_id = PatientConverter.build_fhir_identifier(self.__TEST_CHF_ID,
                                                        Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                        Stu3IdentifierConfig.get_fhir_chfid_type_code())
        identifiers.append(chf_id)
        passport = PatientConverter.build_fhir_identifier(self.__TEST_PASSPORT,
                                                          Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                          Stu3IdentifierConfig.get_fhir_passport_type_code())
        identifiers.append(passport)
        fhir_patient.identifier = identifiers
        fhir_patient.birthDate = self.__TEST_DOB
        fhir_patient.gender = AdministrativeGender.MALE.value
        fhir_patient.maritalStatus = PatientConverter.build_codeable_concept(
            Stu3MaritalConfig.get_fhir_divorced_code(),
            Stu3MaritalConfig.get_fhir_marital_status_system())
        telecom = []
        phone = PatientConverter.build_fhir_contact_point(self.__TEST_PHONE, ContactPointSystem.PHONE.value,
                                                          ContactPointUse.HOME.value)
        telecom.append(phone)
        email = PatientConverter.build_fhir_contact_point(self.__TEST_EMAIL, ContactPointSystem.EMAIL.value,
                                                          ContactPointUse.HOME.value)
        telecom.append(email)
        fhir_patient.telecom = telecom
        addresses = []
        current_address = PatientConverter.build_fhir_address(self.__TEST_ADDRESS, AddressUse.HOME.value,
                                                              AddressType.PHYSICAL.value)
        addresses.append(current_address)
        geolocation = PatientConverter.build_fhir_address(self.__TEST_GEOLOCATION, AddressUse.HOME.value,
                                                          AddressType.BOTH.value)
        addresses.append(geolocation)
        fhir_patient.address = addresses
        return fhir_patient

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(1, len(fhir_obj.name))
        human_name = fhir_obj.name[0]
        self.assertTrue(isinstance(human_name, HumanName))
        self.assertEqual(self.__TEST_OTHER_NAME, human_name.given[0])
        self.assertEqual(self.__TEST_LAST_NAME, human_name.family)
        self.assertEqual(NameUse.USUAL.value, human_name.use)
        self.assertEqual(3, len(fhir_obj.identifier))
        for identifier in fhir_obj.identifier:
            self.assertTrue(isinstance(identifier, Identifier))
            code = PatientConverter.get_first_coding_from_codeable_concept(identifier.type).code
            if code == Stu3IdentifierConfig.get_fhir_chfid_type_code():
                self.assertEqual(self.__TEST_CHF_ID, identifier.value)
            elif code == Stu3IdentifierConfig.get_fhir_id_type_code():
                self.assertEqual(str(self.get_test_db_id()), identifier.value)
            elif code == Stu3IdentifierConfig.get_fhir_passport_type_code():
                self.assertEqual(self.__TEST_PASSPORT, identifier.value)
        self.assertEqual(self.__TEST_DOB, fhir_obj.birthDate)
        self.assertEqual(AdministrativeGender.MALE.value, fhir_obj.gender)
        marital_code = PatientConverter.get_first_coding_from_codeable_concept(fhir_obj.maritalStatus).code
        self.assertEqual(Stu3MaritalConfig.get_fhir_divorced_code(), marital_code)
        self.assertEqual(2, len(fhir_obj.telecom))
        for telecom in fhir_obj.telecom:
            self.assertTrue(isinstance(telecom, ContactPoint))
            if telecom.system == ContactPointSystem.PHONE.value:
                self.assertEqual(self.__TEST_PHONE, telecom.value)
            elif telecom.system == ContactPointSystem.EMAIL.value:
                self.assertEqual(self.__TEST_EMAIL, telecom.value)
        self.assertEqual(2, len(fhir_obj.address))
        for adddress in fhir_obj.address:
            self.assertTrue(isinstance(adddress, Address))
            if adddress.type == AddressType.PHYSICAL.value:
                self.assertEqual(self.__TEST_ADDRESS, adddress.text)
            elif adddress.type == AddressType.BOTH.value:
                self.assertEqual(self.__TEST_GEOLOCATION, adddress.text)
