from claim.models import ClaimAdmin

from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.converters import PractitionerConverter
from api_fhir.models import HumanName, NameUse, Identifier, ContactPoint, ContactPointSystem, Practitioner, \
    ContactPointUse
from api_fhir.tests import GenericTestMixin
from api_fhir.utils import TimeUtils


class PractitionerTestMixin(GenericTestMixin):
    __TEST_LAST_NAME = "Smith"
    __TEST_OTHER_NAME = "John"
    __TEST_DOB = "1990-03-24T00:00:00"
    __TEST_ID = 1
    __TEST_CODE = "1234abcd"
    __TEST_PHONE = "813-996-476"
    __TEST_EMAIL = "TEST@TEST.com"

    def create_test_imis_instance(self):
        imis_claim_admin = ClaimAdmin()
        imis_claim_admin.last_name = self.__TEST_LAST_NAME
        imis_claim_admin.other_names = self.__TEST_OTHER_NAME
        imis_claim_admin.id = self.__TEST_ID
        imis_claim_admin.code = self.__TEST_CODE
        imis_claim_admin.dob = TimeUtils.str_to_date(self.__TEST_DOB)
        imis_claim_admin.phone = self.__TEST_PHONE
        imis_claim_admin.email_id = self.__TEST_EMAIL
        return imis_claim_admin

    def verify_imis_instance(self, imis_obj):
        self.assertEqual(self.__TEST_LAST_NAME, imis_obj.last_name)
        self.assertEqual(self.__TEST_OTHER_NAME, imis_obj.other_names)
        self.assertEqual(self.__TEST_CODE, imis_obj.code)
        expected_date = TimeUtils.str_to_date(self.__TEST_DOB)
        self.assertEqual(expected_date, imis_obj.dob)
        self.assertEqual(self.__TEST_PHONE, imis_obj.phone)
        self.assertEqual(self.__TEST_EMAIL, imis_obj.email_id)

    def create_test_fhir_instance(self):
        fhir_practitioner = Practitioner()
        name = HumanName()
        name.family = self.__TEST_LAST_NAME
        name.given = [self.__TEST_OTHER_NAME]
        name.use = NameUse.USUAL.value
        fhir_practitioner.name = [name]
        identifiers = []
        chf_id = PractitionerConverter.build_fhir_identifier(self.__TEST_CODE,
                                                             Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                             Stu3IdentifierConfig.get_fhir_claim_admin_code_type())
        identifiers.append(chf_id)
        fhir_practitioner.identifier = identifiers
        fhir_practitioner.birthDate = self.__TEST_DOB
        telecom = []
        phone = PractitionerConverter.build_fhir_contact_point(self.__TEST_PHONE, ContactPointSystem.PHONE.value,
                                                               ContactPointUse.HOME.value)
        telecom.append(phone)
        email = PractitionerConverter.build_fhir_contact_point(self.__TEST_EMAIL, ContactPointSystem.EMAIL.value,
                                                               ContactPointUse.HOME.value)
        telecom.append(email)
        fhir_practitioner.telecom = telecom
        return fhir_practitioner

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(1, len(fhir_obj.name))
        human_name = fhir_obj.name[0]
        self.assertTrue(isinstance(human_name, HumanName))
        self.assertEqual(self.__TEST_OTHER_NAME, human_name.given[0])
        self.assertEqual(self.__TEST_LAST_NAME, human_name.family)
        self.assertEqual(NameUse.USUAL.value, human_name.use)
        for identifier in fhir_obj.identifier:
            self.assertTrue(isinstance(identifier, Identifier))
            code = PractitionerConverter.get_first_coding_from_codeable_concept(identifier.type).code
            if code == Stu3IdentifierConfig.get_fhir_claim_admin_code_type():
                self.assertEqual(self.__TEST_CODE, identifier.value)
            elif code == Stu3IdentifierConfig.get_fhir_id_type_code():
                self.assertEqual(str(self.__TEST_ID), identifier.value)
        self.assertEqual(self.__TEST_DOB, fhir_obj.birthDate)
        self.assertEqual(2, len(fhir_obj.telecom))
        for telecom in fhir_obj.telecom:
            self.assertTrue(isinstance(telecom, ContactPoint))
            if telecom.system == ContactPointSystem.PHONE.value:
                self.assertEqual(self.__TEST_PHONE, telecom.value)
            elif telecom.system == ContactPointSystem.EMAIL.value:
                self.assertEqual(self.__TEST_EMAIL, telecom.value)
