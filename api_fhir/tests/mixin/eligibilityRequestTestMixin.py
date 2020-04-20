import uuid

from policy.services import EligibilityResponse

from api_fhir.configurations import Stu3EligibilityConfiguration as Config
from api_fhir.converters import PatientConverter
from api_fhir.models import EligibilityRequest
from api_fhir.tests import GenericTestMixin, PatientTestMixin


class EligibilityRequestTestMixin(GenericTestMixin):

    _TEST_ADMIN_USER_ID = 1
    _TEST_ADMIN_USER_UUID = "90b0cee2-73ae-4705-af8d-8fe035209ab2"
    _TEST_SERVICE_CODE = 'serviceCode'
    _TEST_ITEM_CODE = 'itemCode'
    _TEST_CHFID = 'chfid'
    _TEST_TOTAL_ADMISSIONS = 1
    _TEST_TOTAL_VISITS = 3
    _TEST_TOTAL_CONSULTATIONS = 23
    _TEST_TOTAL_SURGERIES = 5
    _TEST_TOTAL_DELIVERIES = 2
    _TEST_TOTAL_ANTENATAL = 11
    _TEST_CONSULTATION_AMOUNT = 123.21
    _TEST_SURGERY_AMOUNT = 12.11
    _TEST_DELIVERY_AMOUNT = 26.00
    _TEST_HOSPITALIZATION_AMOUNT = 42.00
    _TEST_ANTENATAL_AMOUNT = 59.14
    _TEST_SERVICE_LEFT = 12
    _TEST_ITEM_LEFT = 1
    _TEST_IS_SERVICE_OK = True
    _TEST_IS_ITEM_OK = False

    def setUp(self):
        self._TEST_INSUREE = PatientTestMixin().create_test_imis_instance()
        self._TEST_INSUREE.chf_id = self._TEST_CHFID

    def create_test_imis_instance(self):
        return EligibilityResponse(
            eligibility_request=None,
            prod_id=None,
            total_admissions_left=self._TEST_TOTAL_ADMISSIONS,
            total_visits_left=self._TEST_TOTAL_VISITS,
            total_consultations_left=self._TEST_TOTAL_CONSULTATIONS,
            total_surgeries_left=self._TEST_TOTAL_SURGERIES,
            total_deliveries_left=self._TEST_TOTAL_DELIVERIES,
            total_antenatal_left=self._TEST_TOTAL_ANTENATAL,
            consultation_amount_left=self._TEST_CONSULTATION_AMOUNT,
            surgery_amount_left=self._TEST_SURGERY_AMOUNT,
            delivery_amount_left=self._TEST_DELIVERY_AMOUNT,
            hospitalization_amount_left=self._TEST_HOSPITALIZATION_AMOUNT,
            antenatal_amount_left=self._TEST_ANTENATAL_AMOUNT,
            min_date_service=None,
            min_date_item=None,
            service_left=self._TEST_SERVICE_LEFT,
            item_left=self._TEST_ITEM_LEFT,
            is_item_ok=self._TEST_IS_ITEM_OK,
            is_service_ok=self._TEST_IS_SERVICE_OK
        )

    def verify_imis_instance(self, imis_obj):
        # The reference used to be the CHFID but reference are now all on UUID
        # self.assertEqual(self._TEST_CHFID, imis_obj.chf_id)
        self.assertEqual(str(self._TEST_INSUREE.uuid), imis_obj.chf_id)
        self.assertEqual(self._TEST_ITEM_CODE, imis_obj.item_code)
        self.assertEqual(self._TEST_SERVICE_CODE, imis_obj.service_code)

    def create_test_fhir_instance(self):
        self.setUp()
        fhir_reqest = EligibilityRequest()
        fhir_reqest.patient = PatientConverter.build_fhir_resource_reference(self._TEST_INSUREE)
        fhir_reqest.benefitCategory = PatientConverter.build_codeable_concept(
            Config.get_fhir_service_code(), system=None, text=self._TEST_SERVICE_CODE)
        fhir_reqest.benefitSubCategory = PatientConverter.build_codeable_concept(
            Config.get_fhir_item_code(), system=None, text=self._TEST_ITEM_CODE)
        return fhir_reqest

    def verify_fhir_instance(self, fhir_obj):
        self.assertIsNotNone(fhir_obj.insurance[0].benefitBalance)
        for benefit in fhir_obj.insurance[0].benefitBalance:
            if benefit.category.text == Config.get_fhir_total_admissions_code():
                self.assertEqual(self._TEST_TOTAL_ADMISSIONS, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_total_visits_code():
                self.assertEqual(self._TEST_TOTAL_VISITS, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_total_consultations_code():
                self.assertEqual(self._TEST_TOTAL_CONSULTATIONS, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_total_surgeries_code():
                self.assertEqual(self._TEST_TOTAL_SURGERIES, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_total_deliveries_code():
                self.assertEqual(self._TEST_TOTAL_DELIVERIES, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_total_antenatal_code():
                self.assertEqual(self._TEST_TOTAL_ANTENATAL, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_consultation_amount_code():
                self.assertEqual(self._TEST_CONSULTATION_AMOUNT, benefit.financial[0].allowedMoney.value)
            elif benefit.category.text == Config.get_fhir_surgery_amount_code():
                self.assertEqual(self._TEST_SURGERY_AMOUNT, benefit.financial[0].allowedMoney.value)
            elif benefit.category.text == Config.get_fhir_delivery_amount_code():
                self.assertEqual(self._TEST_DELIVERY_AMOUNT, benefit.financial[0].allowedMoney.value)
            elif benefit.category.text == Config.get_fhir_hospitalization_amount_code():
                self.assertEqual(self._TEST_HOSPITALIZATION_AMOUNT, benefit.financial[0].allowedMoney.value)
            elif benefit.category.text == Config.get_fhir_antenatal_amount_code():
                self.assertEqual(self._TEST_ANTENATAL_AMOUNT, benefit.financial[0].allowedMoney.value)
            elif benefit.category.text == Config.get_fhir_service_left_code():
                self.assertEqual(self._TEST_SERVICE_LEFT, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_item_left_code():
                self.assertEqual(self._TEST_ITEM_LEFT, benefit.financial[0].allowedUnsignedInt)
            elif benefit.category.text == Config.get_fhir_is_service_ok_code():
                self.assertEqual(self._TEST_IS_SERVICE_OK, not benefit.excluded)
            elif benefit.category.text == Config.get_fhir_is_item_ok_code():
                self.assertEqual(self._TEST_IS_ITEM_OK, not benefit.excluded)
