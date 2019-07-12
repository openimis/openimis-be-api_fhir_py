from claim.models import Claim, ClaimDiagnosisCode

from api_fhir.configurations import Stu3IdentifierConfig, Stu3ClaimConfig
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
    _TEST_EXPLANATION = "explanation"
    _TEST_ICD_1 = "icd_1"
    _TEST_ICD_2 = "icd_2"
    _TEST_ICD_3 = "icd_3"
    _TEST_ICD_4 = "icd_4"
    _TEST_VISIT_TYPE = "E"

    def setUp(self):
        self._TEST_DIAGNOSIS_CODE = ClaimDiagnosisCode()
        self._TEST_DIAGNOSIS_CODE.code = self._TEST_MAIN_ICD_CODE
        self._TEST_CLAIM_ADMIN = PractitionerTestMixin().create_test_imis_instance()
        self._TEST_HF = LocationTestMixin().create_test_imis_instance()
        self._TEST_INSUREE = PatientTestMixin().create_test_imis_instance()

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
        self.assertEqual(self._TEST_EXPLANATION, imis_obj.explanation)
        self.assertIsNotNone(imis_obj.admin)
        self.assertEqual(self._TEST_VISIT_TYPE, imis_obj.visit_type)

    def create_test_fhir_instance(self):
        self.setUp()
        fhir_claim = FHIRClaim()
        fhir_claim.patient = PatientConverter.build_fhir_resource_reference(self._TEST_INSUREE)
        claim_code = ClaimConverter.build_fhir_identifier(self._TEST_CODE,
                                               Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                               Stu3IdentifierConfig.get_fhir_claim_code_type())
        fhir_claim.identifier = [claim_code]
        billable_period = Period()
        billable_period.start = self._TEST_DATE_FROM
        billable_period.end = self._TEST_DATE_TO
        fhir_claim.billablePeriod = billable_period
        diagnoses = []
        ClaimConverter.build_fhir_diagnosis(diagnoses, self._TEST_DIAGNOSIS_CODE.code, ImisClaimIcdTypes.ICD_0.value)
        fhir_claim.diagnosis = diagnoses
        total = Money()
        total.value = self._TEST_CLAIMED
        fhir_claim.total = total
        fhir_claim.created = self._TEST_DATE_CLAIMED
        fhir_claim.facility = LocationConverter.build_fhir_resource_reference(self._TEST_HF)
        information = []
        guarantee_id_code = Stu3ClaimConfig.get_fhir_claim_information_guarantee_id_code()
        ClaimConverter.build_fhir_string_information(information, guarantee_id_code, self._TEST_GUARANTEE_ID)
        explanation_code = Stu3ClaimConfig.get_fhir_claim_information_explanation_code()
        ClaimConverter.build_fhir_string_information(information, explanation_code, self._TEST_EXPLANATION)
        fhir_claim.information = information
        fhir_claim.enterer = PractitionerConverter.build_fhir_resource_reference(self._TEST_CLAIM_ADMIN)
        fhir_claim.type = ClaimConverter.build_simple_codeable_concept(self._TEST_VISIT_TYPE)
        return fhir_claim

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
        for information in fhir_obj.information:
            if information.category.text == Stu3ClaimConfig.get_fhir_claim_information_explanation_code():
                self.assertEqual(self._TEST_EXPLANATION, information.valueString)
            elif information.category.text == Stu3ClaimConfig.get_fhir_claim_information_guarantee_id_code():
                self.assertEqual(self._TEST_GUARANTEE_ID, information.valueString)
        self.assertIsNotNone(fhir_obj.enterer.reference)
        self.assertEqual(self._TEST_VISIT_TYPE, fhir_obj.type.text)
