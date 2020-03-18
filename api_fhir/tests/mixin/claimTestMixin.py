from claim.models import Claim, ClaimItem, ClaimService
from medical.models import Diagnosis
from medical.models import Item, Service

from api_fhir.configurations import Stu3IdentifierConfig, Stu3ClaimConfig
from api_fhir.converters import PatientConverter, LocationConverter, PractitionerConverter
from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.models import Claim as FHIRClaim, ImisClaimIcdTypes, Period, Money
from api_fhir.tests import GenericTestMixin, PatientTestMixin, LocationTestMixin, PractitionerTestMixin
from api_fhir.utils import TimeUtils


class ClaimTestMixin(GenericTestMixin):

    _TEST_ID = 1
    _TEST_UUID = "315c3b16-62eb-11ea-8e75-df3492b349f6"
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
    _TEST_ITEM_CODE = "iCode"
    _TEST_ITEM_QUANTITY_PROVIDED = 4
    _TEST_ITEM_PRICE_ASKED = 21.1
    _TEST_ITEM_EXPLANATION = "item_explanation"
    _TEST_SERVICE_CODE = "sCode"
    _TEST_SERVICE_QUANTITY_PROVIDED = 3
    _TEST_SERVICE_PRICE_ASKED = 16.1
    _TEST_SERVICE_EXPLANATION = "service_explanation"

    def setUp(self):
        self._TEST_DIAGNOSIS_CODE = Diagnosis()
        self._TEST_DIAGNOSIS_CODE.code = self._TEST_MAIN_ICD_CODE
        self._TEST_CLAIM_ADMIN = PractitionerTestMixin().create_test_imis_instance()
        self._TEST_HF = LocationTestMixin().create_test_imis_instance()
        self._TEST_INSUREE = PatientTestMixin().create_test_imis_instance()
        self._TEST_ITEM = self.create_test_claim_item()
        self._TEST_SERVICE = self.create_test_claim_service()

    def create_test_claim_item(self):
        item = ClaimItem()
        item.item = Item()
        item.item.code = self._TEST_ITEM_CODE
        item.price_asked = self._TEST_ITEM_PRICE_ASKED
        item.qty_provided = self._TEST_ITEM_QUANTITY_PROVIDED
        item.explanation = self._TEST_ITEM_EXPLANATION
        return item

    def create_test_claim_service(self):
        service = ClaimService()
        service.service = Service()
        service.service.code = self._TEST_SERVICE_CODE
        service.price_asked = self._TEST_SERVICE_PRICE_ASKED
        service.qty_provided = self._TEST_SERVICE_QUANTITY_PROVIDED
        service.explanation = self._TEST_SERVICE_EXPLANATION
        return service

    def create_test_imis_instance(self):
        imis_claim = Claim()
        imis_claim.id = self._TEST_ID
        imis_claim.uuid = self._TEST_UUID
        imis_claim.insuree = PatientTestMixin().create_test_imis_instance()
        imis_claim.code = self._TEST_CODE
        imis_claim.date_from = TimeUtils.str_to_date(self._TEST_DATE_FROM)
        imis_claim.date_to = TimeUtils.str_to_date(self._TEST_DATE_TO)
        icd = Diagnosis()
        icd.code = self._TEST_MAIN_ICD_CODE
        imis_claim.icd = icd
        imis_claim.claimed = self._TEST_CLAIMED
        imis_claim.date_claimed = TimeUtils.str_to_date(self._TEST_DATE_CLAIMED)
        imis_claim.health_facility = LocationTestMixin().create_test_imis_instance()
        imis_claim.guarantee_id = self._TEST_GUARANTEE_ID
        imis_claim.admin = PractitionerTestMixin().create_test_imis_instance()
        imis_claim.icd_1 = Diagnosis(code=self._TEST_ICD_1)
        imis_claim.icd_2 = Diagnosis(code=self._TEST_ICD_2)
        imis_claim.icd_3 = Diagnosis(code=self._TEST_ICD_3)
        imis_claim.icd_4 = Diagnosis(code=self._TEST_ICD_4)
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
        self.assertEqual(self._TEST_ITEM_CODE, imis_obj.submit_items[0].code)
        self.assertEqual(self._TEST_ITEM_QUANTITY_PROVIDED, imis_obj.submit_items[0].quantity)
        self.assertEqual(self._TEST_ITEM_PRICE_ASKED, imis_obj.submit_items[0].price)
        self.assertEqual(self._TEST_SERVICE_CODE, imis_obj.submit_services[0].code)
        self.assertEqual(self._TEST_SERVICE_QUANTITY_PROVIDED, imis_obj.submit_services[0].quantity)
        self.assertEqual(self._TEST_SERVICE_PRICE_ASKED, imis_obj.submit_services[0].price)

    def create_test_fhir_instance(self):
        fhir_claim = FHIRClaim()
        fhir_claim.id = self._TEST_UUID
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
        type = Stu3ClaimConfig.get_fhir_claim_item_code()
        ClaimConverter.build_fhir_item(fhir_claim, self._TEST_ITEM_CODE, type, self._TEST_ITEM)
        type = Stu3ClaimConfig.get_fhir_claim_service_code()
        ClaimConverter.build_fhir_item(fhir_claim, self._TEST_SERVICE_CODE, type, self._TEST_SERVICE)
        return fhir_claim

    def verify_fhir_instance(self, fhir_obj):
        self.assertIsNotNone(fhir_obj.patient.reference)
        self.assertEqual(str(self._TEST_UUID), fhir_obj.id)
        for identifier in fhir_obj.identifier:
            if identifier.type.coding[0].code == Stu3IdentifierConfig.get_fhir_uuid_type_code():
                self.assertEqual(fhir_obj.id, identifier.value)
            elif identifier.type.coding[0].code == Stu3IdentifierConfig.get_fhir_claim_code_type():
                self.assertEqual(self._TEST_CODE, identifier.value)

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
        for item in fhir_obj.item:
            if item.category.text == Stu3ClaimConfig.get_fhir_claim_item_code():
                self.assertEqual(self._TEST_ITEM_CODE, item.service.text)
                self.assertEqual(self._TEST_ITEM_QUANTITY_PROVIDED, item.quantity.value)
                self.assertEqual(self._TEST_ITEM_PRICE_ASKED, item.unitPrice.value)
                self.assertEqual(self._TEST_ITEM_EXPLANATION,
                                 fhir_obj.information[item.informationLinkId[0] - 1].valueString)
            elif item.category.text == Stu3ClaimConfig.get_fhir_claim_service_code():
                self.assertEqual(self._TEST_SERVICE_CODE, item.service.text)
                self.assertEqual(self._TEST_SERVICE_QUANTITY_PROVIDED, item.quantity.value)
                self.assertEqual(self._TEST_SERVICE_PRICE_ASKED, item.unitPrice.value)
                self.assertEqual(self._TEST_SERVICE_EXPLANATION,
                                 fhir_obj.information[item.informationLinkId[0] - 1].valueString)
