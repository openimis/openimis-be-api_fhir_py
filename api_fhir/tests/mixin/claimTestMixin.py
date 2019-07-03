from claim.models import Claim, ClaimDiagnosisCode

from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.converters import PatientConverter, LocationConverter, PractitionerConverter
from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.models import Claim as FHIRClaim, ImisClaimIcdTypes, Period, Money
from api_fhir.tests import GenericTestMixin, PatientTestMixin, LocationTestMixin, PractitionerTestMixin
from api_fhir.utils import TimeUtils


class ClaimTestMixin(GenericTestMixin):

    _TEST_CODE = 'code'
    _TEST_DATE_FROM = '2019-06-01T00:00:00'
    _TEST_DATE_TO = '2019-06-12T00:00:00'
    _TEST_MAIN_ICD_CODE = 'ICD_CD'
    _TEST_CLAIMED = 42
    _TEST_DATE_CLAIMED = '2019-06-12T00:00:00'
    _TEST_GUARANTEE_ID = "guarantee_id"
    _TEST_ICD_1 = "icd_1"
    _TEST_ICD_2 = "icd_2"
    _TEST_ICD_3 = "icd_3"
    _TEST_ICD_4 = "icd_4"
    _TEST_VISIT_TYPE = "E"
    _TEST_ADMIN_USER_ID = 1

    def create_test_imis_instance(self):
        imis_claim = Claim()
        imis_claim.insuree = PatientTestMixin().create_test_imis_instance()
        imis_claim.code = self._TEST_CODE
        imis_claim.date_from = TimeUtils.str_to_date(self._TEST_DATE_FROM)
        imis_claim.date_to = TimeUtils.str_to_date(self._TEST_DATE_TO)
        icd = ClaimDiagnosisCode()
        icd.code = self._TEST_MAIN_ICD_CODE
        imis_claim.icd = icd
        imis_claim.claimed = self._TEST_CLAIMED
        imis_claim.date_claimed = TimeUtils.str_to_date(self._TEST_DATE_CLAIMED)
        imis_claim.health_facility = LocationTestMixin().create_test_imis_instance()
        imis_claim.guarantee_id = self._TEST_GUARANTEE_ID
        imis_claim.admin = PractitionerTestMixin().create_test_imis_instance()
        imis_claim.icd_1 = self._TEST_ICD_1
        imis_claim.icd_2 = self._TEST_ICD_2
        imis_claim.icd_3 = self._TEST_ICD_3
        imis_claim.icd_4 = self._TEST_ICD_4
        imis_claim.visit_type = self._TEST_VISIT_TYPE
        return imis_claim

    def verify_imis_instance(self, imis_obj):
        self.assertIsNotNone(imis_obj.insuree)
        self.assertEqual(self._TEST_CODE, imis_obj.code)
        self.assertEqual(self._TEST_DATE_FROM, imis_obj.date_from.isoformat())
        self.assertEqual(self._TEST_DATE_TO, imis_obj.date_to.isoformat())
        self.assertEqual(self._TEST_MAIN_ICD_CODE, imis_obj.icd.code)
        self.assertEqual(self._TEST_CLAIMED, imis_obj.claimed)
        self.assertEqual(self._TEST_DATE_CLAIMED, imis_obj.date_claimed.isoformat())
        self.assertIsNotNone(imis_obj.health_facility)
        self.assertEqual(self._TEST_GUARANTEE_ID, imis_obj.guarantee_id)
        self.assertIsNotNone(imis_obj.admin)
        self.assertEqual(self._TEST_VISIT_TYPE, imis_obj.visit_type)

    def create_test_fhir_instance(self):
        fhir_claim = FHIRClaim()
        imis_insuree = self._create_and_save_insuree()
        fhir_claim.patient = PatientConverter.build_fhir_resource_reference(imis_insuree)
        claim_code = ClaimConverter.build_fhir_identifier(self._TEST_CODE,
                                               Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                               Stu3IdentifierConfig.get_fhir_claim_code_type())
        fhir_claim.identifier = [claim_code]
        billable_period = Period()
        billable_period.start = self._TEST_DATE_FROM
        billable_period.end = self._TEST_DATE_TO
        fhir_claim.billablePeriod = billable_period
        diagnoses = []
        diagnosis_code = self._create_and_save_diagnosis_code()
        ClaimConverter.build_fhir_diagnosis(diagnoses, diagnosis_code.code, ImisClaimIcdTypes.ICD_0.value)
        fhir_claim.diagnosis = diagnoses
        total = Money()
        total.value = self._TEST_CLAIMED
        fhir_claim.total = total
        fhir_claim.created = self._TEST_DATE_CLAIMED
        imis_hf = self._create_and_save_hf()
        fhir_claim.facility = LocationConverter.build_fhir_resource_reference(imis_hf)
        information = []
        ClaimConverter.build_fhir_guarantee_id_information(information, self._TEST_GUARANTEE_ID)
        fhir_claim.information = information
        claim_admin = self._create_and_save_claim_admin()
        fhir_claim.enterer = PractitionerConverter.build_fhir_resource_reference(claim_admin)
        fhir_claim.type = ClaimConverter.build_simple_codeable_concept(self._TEST_VISIT_TYPE)
        return fhir_claim

    def _create_and_save_diagnosis_code(self):
        diagnosis_code = ClaimDiagnosisCode()
        diagnosis_code.code = self._TEST_MAIN_ICD_CODE
        diagnosis_code.validity_from = TimeUtils.now()
        diagnosis_code.audit_user_id = self._TEST_ADMIN_USER_ID
        diagnosis_code.save()
        return diagnosis_code

    def _create_and_save_claim_admin(self):
        claim_admin = PractitionerTestMixin().create_test_imis_instance()
        claim_admin.save()
        return claim_admin

    def _create_and_save_hf(self):
        imis_hf = LocationTestMixin().create_test_imis_instance()
        imis_hf.validity_from = TimeUtils.now()
        imis_hf.offline = False
        imis_hf.audit_user_id = self._TEST_ADMIN_USER_ID
        imis_hf.save()
        return imis_hf

    def _create_and_save_insuree(self):
        imis_insuree = PatientTestMixin().create_test_imis_instance()
        imis_insuree.head = False
        imis_insuree.card_issued = False
        imis_insuree.validity_from = TimeUtils.now()
        imis_insuree.audit_user_id = self._TEST_ADMIN_USER_ID
        imis_insuree.save()
        return imis_insuree

    def verify_fhir_instance(self, fhir_obj):
        self.assertIsNotNone(fhir_obj.patient.reference)
        self.assertEqual(self._TEST_CODE, fhir_obj.identifier[0].value)
        self.assertEqual(self._TEST_DATE_FROM, fhir_obj.billablePeriod.start)
        self.assertEqual(self._TEST_DATE_TO, fhir_obj.billablePeriod.end)
        for diagnosis in fhir_obj.diagnosis:
            type = diagnosis.type[0].text
            code = diagnosis.diagnosisCodeableConcept.coding[0].code
            if type == ImisClaimIcdTypes.ICD_0.value:
                self.assertEqual(self._TEST_MAIN_ICD_CODE, code)

        self.assertEqual(self._TEST_CLAIMED, fhir_obj.total.value)
        self.assertEqual(self._TEST_DATE_CLAIMED, fhir_obj.created)
        self.assertIsNotNone(fhir_obj.facility.reference)
        self.assertEqual(self._TEST_GUARANTEE_ID, fhir_obj.information[0].valueString)
        self.assertIsNotNone(fhir_obj.enterer.reference)
        self.assertEqual(self._TEST_VISIT_TYPE, fhir_obj.type.text)
