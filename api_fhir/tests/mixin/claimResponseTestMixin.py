from claim.models import Claim, Feedback

from api_fhir.configurations import Stu3IdentifierConfig, Stu3ClaimConfig
from api_fhir.converters import ClaimResponseConverter, CommunicationRequestConverter
from api_fhir.models import ClaimResponse, ClaimResponsePayment, Money, ClaimResponseError
from api_fhir.tests import GenericTestMixin
from api_fhir.utils import TimeUtils


class ClaimResponseTestMixin(GenericTestMixin):

    _TEST_CODE = 'code'
    _TEST_STATUS = '1'
    _TEST_ADJUSTMENT = "adjustment"
    _TEST_DATE_PROCESSED = "2010-11-16T00:00:00"
    _TEST_APPROVED = 214.25
    _TEST_REJECTION_REASON = '1'
    _TEST_FEEDBACK_ID = 1

    def create_test_imis_instance(self):
        imis_claim = Claim()
        imis_claim.code = self._TEST_CODE
        imis_claim.status = self._TEST_STATUS
        imis_claim.adjustment = self._TEST_ADJUSTMENT
        imis_claim.date_processed = TimeUtils.str_to_date(self._TEST_DATE_PROCESSED)
        imis_claim.approved = self._TEST_APPROVED
        imis_claim.rejection_reason = self._TEST_REJECTION_REASON
        feedback = Feedback()
        feedback.id = self._TEST_FEEDBACK_ID
        imis_claim.feedback = feedback
        return imis_claim

    def create_test_fhir_instance(self):
        fhir_claim_response = ClaimResponse()
        claim_code = ClaimResponseConverter.build_fhir_identifier(self._TEST_CODE,
                                                          Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                          Stu3IdentifierConfig.get_fhir_claim_code_type())
        fhir_claim_response.identifier = [claim_code]
        display = Stu3ClaimConfig.get_fhir_claim_status_rejected_code()
        fhir_claim_response.outcome = ClaimResponseConverter.build_codeable_concept(self._TEST_STATUS, system=None,
                                                                                    text=display)
        fhir_payment = ClaimResponsePayment()
        fhir_payment.adjustmentReason = ClaimResponseConverter.build_simple_codeable_concept(self._TEST_ADJUSTMENT)
        fhir_payment.date = self._TEST_DATE_PROCESSED
        fhir_claim_response.payment = fhir_payment
        total_approved = Money()
        total_approved.value = self._TEST_APPROVED
        fhir_claim_response.totalBenefit = total_approved
        fhir_error = ClaimResponseError()
        fhir_error.code = ClaimResponseConverter.build_codeable_concept(self._TEST_REJECTION_REASON)
        fhir_claim_response.error = [fhir_error]
        feedback = Feedback()
        feedback.id = self._TEST_FEEDBACK_ID
        fhir_claim_response.communicationRequest = \
            [CommunicationRequestConverter.build_fhir_resource_reference(feedback)]
        return fhir_claim_response

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(self._TEST_CODE, fhir_obj.identifier[0].value)
        self.assertEqual(self._TEST_STATUS, fhir_obj.outcome.coding[0].code)
        self.assertEqual(self._TEST_ADJUSTMENT, fhir_obj.payment.adjustmentReason.text)
        self.assertEqual(self._TEST_DATE_PROCESSED, fhir_obj.payment.date)
        self.assertEqual(self._TEST_APPROVED, fhir_obj.totalBenefit.value)
        self.assertEqual(self._TEST_REJECTION_REASON, fhir_obj.error[0].code.coding[0].code)
        self.assertEqual(str(self._TEST_FEEDBACK_ID), CommunicationRequestConverter.get_resource_id_from_reference(
            fhir_obj.communicationRequest[0]))
