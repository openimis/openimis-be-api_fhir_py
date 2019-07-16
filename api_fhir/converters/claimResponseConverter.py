from api_fhir.configurations import Stu3ClaimConfig
from api_fhir.converters import BaseFHIRConverter, CommunicationRequestConverter
from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.models import ClaimResponse, Money, ClaimResponsePayment, ClaimResponseError
from api_fhir.utils import TimeUtils


class ClaimResponseConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim):
        fhir_claim_response = ClaimResponse()
        fhir_claim_response.created = TimeUtils.date().isoformat()
        fhir_claim_response.request = ClaimConverter.build_fhir_resource_reference(imis_claim)
        cls.build_fhir_pk(fhir_claim_response, imis_claim.code)
        ClaimConverter.build_fhir_identifiers(fhir_claim_response, imis_claim)
        cls.build_fhir_outcome(fhir_claim_response, imis_claim)
        cls.build_fhir_payment(fhir_claim_response, imis_claim)
        cls.build_fhir_total_benefit(fhir_claim_response, imis_claim)
        cls.build_fhir_errors(fhir_claim_response, imis_claim)
        cls.build_fhir_communication_request_reference(fhir_claim_response, imis_claim)
        return fhir_claim_response

    @classmethod
    def build_fhir_outcome(cls, fhir_claim_response, imis_claim):
        code = imis_claim.status
        if code is not None:
            display = None
            if code == 1:
                display = Stu3ClaimConfig.get_fhir_claim_status_rejected_code()
            elif code == 2:
                display = Stu3ClaimConfig.get_fhir_claim_status_entered_code()
            elif code == 4:
                display = Stu3ClaimConfig.get_fhir_claim_status_checked_code()
            elif code == 8:
                display = Stu3ClaimConfig.get_fhir_claim_status_processed_code()
            elif code == 16:
                display = Stu3ClaimConfig.get_fhir_claim_status_valuated_code()
            fhir_claim_response.outcome = cls.build_codeable_concept(imis_claim.status, system=None, text=display)

    @classmethod
    def build_fhir_payment(cls, fhir_claim_response, imis_claim):
        fhir_payment = ClaimResponsePayment()
        fhir_payment.adjustmentReason = cls.build_simple_codeable_concept(imis_claim.adjustment)
        fhir_payment.date = imis_claim.date_processed.isoformat()
        fhir_claim_response.payment = fhir_payment

    @classmethod
    def build_fhir_total_benefit(cls, fhir_claim_response, imis_claim):
        total_approved = Money()
        total_approved.value = imis_claim.approved
        fhir_claim_response.totalBenefit = total_approved

    @classmethod
    def build_fhir_errors(cls, fhir_claim_response, imis_claim):
        rejection_reason = imis_claim.rejection_reason
        if rejection_reason:
            fhir_error = ClaimResponseError()
            fhir_error.code = cls.build_codeable_concept(rejection_reason)
            fhir_claim_response.error = [fhir_error]

    @classmethod
    def build_fhir_communication_request_reference(cls, fhir_claim_response, imis_claim):
        feedback = imis_claim.feedback
        if feedback:
            reference = CommunicationRequestConverter.build_fhir_resource_reference(feedback)
            fhir_claim_response.communicationRequest = [reference]
