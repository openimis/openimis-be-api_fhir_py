from claim.models import Feedback, ClaimItem, ClaimService
from django.db.models import Subquery
from medical.models import Item, Service
import core

from api_fhir_R4.configurations import R4ClaimConfig
from api_fhir_R4.converters import BaseFHIRConverter, CommunicationRequestConverter
from api_fhir_R4.converters.claimConverter import ClaimConverter
from api_fhir_R4.converters.patientConverter import PatientConverter
from api_fhir_R4.exceptions import FHIRRequestProcessException
from api_fhir_R4.models import ClaimResponse, Money, ClaimResponsePayment, ClaimResponseError, ClaimResponseItem, Claim, \
    ClaimResponseItemAdjudication, ClaimResponseProcessNote, ClaimResponseAddItem, ClaimResponseTotal
from api_fhir_R4.utils import TimeUtils, FhirUtils


class ClaimResponseConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim):
        fhir_claim_response = ClaimResponse()
        fhir_claim_response.created = TimeUtils.date().isoformat()
        fhir_claim_response.request = ClaimConverter.build_fhir_resource_reference(imis_claim)
        cls.build_fhir_pk(fhir_claim_response, imis_claim.uuid)
        ClaimConverter.build_fhir_identifiers(fhir_claim_response, imis_claim)
        cls.build_fhir_outcome(fhir_claim_response, imis_claim)
        #cls.build_fhir_payment(fhir_claim_response, imis_claim)
        #cls.build_fhir_total_benefit(fhir_claim_response, imis_claim)
        cls.build_fhir_errors(fhir_claim_response, imis_claim)
        #cls.build_fhir_request_reference(fhir_claim_response, imis_claim)
        cls.build_fhir_items(fhir_claim_response, imis_claim)
        cls.build_patient_reference(fhir_claim_response, imis_claim)
        cls.build_fhir_total(fhir_claim_response, imis_claim)
        cls.build_fhir_communication_request_reference(fhir_claim_response, imis_claim)
        return fhir_claim_response

    @classmethod
    def build_fhir_outcome(cls, fhir_claim_response, imis_claim):
        code = imis_claim.status
        if code is not None:
            display = cls.get_status_display_by_code(code)
            fhir_claim_response.outcome = cls.build_codeable_concept(str(code), system=None, text=display)

    @classmethod
    def get_status_display_by_code(cls, code):
        display = None
        if code == 1:
            display = R4ClaimConfig.get_fhir_claim_status_rejected_code()
        elif code == 2:
            display = R4ClaimConfig.get_fhir_claim_status_entered_code()
        elif code == 4:
            display = R4ClaimConfig.get_fhir_claim_status_checked_code()
        elif code == 8:
            display = R4ClaimConfig.get_fhir_claim_status_processed_code()
        elif code == 16:
            display = R4ClaimConfig.get_fhir_claim_status_valuated_code()
        return display

    """
    @classmethod
    def build_fhir_payment(cls, fhir_claim_response, imis_claim):
        fhir_payment = ClaimResponsePayment()
        fhir_payment.adjustmentReason = cls.build_simple_codeable_concept(imis_claim.adjustment)
        date_processed = imis_claim.date_processed
        if date_processed:
            fhir_payment.date = date_processed.isoformat()
        fhir_claim_response.payment = fhir_payment
    """
    """
    @classmethod
    def build_fhir_total_benefit(cls, fhir_claim_response, imis_claim):
        total_approved = Money()
        total_approved.value = imis_claim.approved
        fhir_claim_response.totalBenefit = total_approved
    """

    @classmethod
    def build_fhir_errors(cls, fhir_claim_response, imis_claim):
        rejection_reason = imis_claim.rejection_reason
        if rejection_reason:
            fhir_error = ClaimResponseError()
            fhir_error.code = cls.build_codeable_concept(str(rejection_reason))
            fhir_claim_response.error = [fhir_error]

    @classmethod
    def build_fhir_request_reference(cls, fhir_claim_response, imis_claim):
        feedback = cls.get_imis_claim_feedback(imis_claim)
        if feedback:
            reference = CommunicationRequestConverter.build_fhir_resource_reference(feedback)
            fhir_claim_response.communicationRequest = [reference]

    @classmethod
    def get_imis_claim_feedback(cls, imis_claim):
        try:
            feedback = imis_claim.feedback
        except Feedback.DoesNotExist:
            feedback = None
        return feedback

    @classmethod
    def build_fhir_items(cls, fhir_claim_response, imis_claim):
        for claim_item in cls.generate_fhir_claim_items(imis_claim):
            type = claim_item.category.text
            code = claim_item.productOrService.text

            if type == R4ClaimConfig.get_fhir_claim_item_code():
                serviced = cls.get_imis_claim_item_by_code(code, imis_claim.id)
            elif type == R4ClaimConfig.get_fhir_claim_service_code():
                serviced = cls.get_service_claim_item_by_code(code, imis_claim.id)
            else:
                raise FHIRRequestProcessException(['Could not assign category {} for claim_item: {}'
                                                  .format(type, claim_item)])

            #cls._build_response_items(fhir_claim_response, claim_item, serviced, serviced.rejection_reason)

    @classmethod
    def _build_response_items(cls, fhir_claim_response, claim_item, imis_service, rejected_reason):
        cls.build_fhir_item(fhir_claim_response, claim_item, imis_service,
                            rejected_reason=rejected_reason)
        cls.build_fhir_claim_add_item(fhir_claim_response, claim_item)

    @classmethod
    def generate_fhir_claim_items(cls, imis_claim):
        claim = Claim()
        ClaimConverter.build_fhir_items(claim, imis_claim)
        return claim.item

    @classmethod
    def get_imis_claim_item_by_code(cls, code, imis_claim_id):
        item_code_qs = Item.objects.filter(code=code)
        result = ClaimItem.objects.filter(item_id__in=Subquery(item_code_qs.values('id')), claim_id=imis_claim_id)
        return result[0] if len(result) > 0 else None

    @classmethod
    def build_fhir_claim_add_item(cls, fhir_claim_response, claim_item):
        add_item = ClaimResponseAddItem()
        item_code = claim_item.productOrService.text
        add_item.itemSequence.append(claim_item.sequence)
        add_item.productOrService = cls.build_codeable_concept(code=item_code)
        fhir_claim_response.addItem.append(add_item)

    @classmethod
    def get_service_claim_item_by_code(cls, code, imis_claim_id):
        service_code_qs = Service.objects.filter(code=code)
        result = ClaimService.objects.filter(service_id__in=Subquery(service_code_qs.values('id')),
                                             claim_id=imis_claim_id)
        return result[0] if len(result) > 0 else None

    @classmethod
    def build_fhir_item(cls, fhir_claim_response, claim_item, item, rejected_reason=None):
        claim_response_item = ClaimResponseItem()
        claim_response_item.itemSequence = claim_item.sequence
        cls.build_fhir_item_general_adjudication(claim_response_item, item)
        if rejected_reason:
            cls.build_fhir_item_rejected_reason_adjudication(claim_response_item, rejected_reason)
        note = cls.build_process_note(fhir_claim_response, item.justification)
        if note:
            claim_response_item.noteNumber = [note.number]
        fhir_claim_response.item.append(claim_response_item)

    @classmethod
    def build_fhir_item_general_adjudication(cls, claim_response_item, item):
        item_adjudication = ClaimResponseItemAdjudication()
        item_adjudication.category = \
            cls.build_simple_codeable_concept(R4ClaimConfig.get_fhir_claim_item_general_adjudication_code())
        item_adjudication.reason = cls.build_fhir_adjudication_reason(item)
        item_adjudication.value = item.qty_approved
        price_valuated = Money()
        price_valuated.value = item.price_valuated
        item_adjudication.amount = price_valuated
        claim_response_item.adjudication.append(item_adjudication)

    @classmethod
    def build_fhir_item_rejected_reason_adjudication(cls, claim_response_item, rejection_reason):
        item_adjudication = ClaimResponseItemAdjudication()
        item_adjudication.category = \
            cls.build_simple_codeable_concept(R4ClaimConfig.get_fhir_claim_item_rejected_reason_adjudication_code())
        item_adjudication.reason = cls.build_codeable_concept(rejection_reason)
        claim_response_item.adjudication.append(item_adjudication)

    @classmethod
    def build_fhir_adjudication_reason(cls, item):
        status = item.status
        text_code = None
        if status == 1:
            text_code = R4ClaimConfig.get_fhir_claim_item_status_passed_code()
        elif status == 2:
            text_code = R4ClaimConfig.get_fhir_claim_item_status_rejected_code()
        return cls.build_codeable_concept(status, text=text_code)

    @classmethod
    def build_process_note(cls, fhir_claim_response, string_value):
        result = None
        if string_value:
            note = ClaimResponseProcessNote()
            note.number = FhirUtils.get_next_array_sequential_id(fhir_claim_response.processNote)
            note.text = string_value
            fhir_claim_response.processNote.append(note)
            result = note
        return result

    @classmethod
    def build_patient_reference(cls, fhir_claim_response, imis_claim):
        fhir_claim_response.patient = PatientConverter.build_fhir_resource_reference(imis_claim.insuree)

    @classmethod
    def build_fhir_total(cls, fhir_claim_response, imis_claim):
        valuated = cls.build_fhir_total_valuated(imis_claim)
        reinsured = cls.build_fhir_total_reinsured(imis_claim)
        approved = cls.build_fhir_total_approved(imis_claim)
        claimed = cls.build_fhir_total_claimed(imis_claim)

        if valuated.amount.value is not None and reinsured.amount.value is None and \
                approved.amount.value is None and claimed.amount.value is None:
            fhir_claim_response.total = [valuated]

        elif valuated.amount.value is None and reinsured.amount.value is not None and \
                approved.amount.value is None and claimed.amount.value is None:
            fhir_claim_response.total = [reinsured]

        elif valuated.amount.value is None and reinsured.amount.value is None and \
                approved.amount.value is not None and claimed.amount.value is None:
            fhir_claim_response.total = [approved]

        elif valuated.amount.value is None and reinsured.amount.value is None and \
                approved.amount.value is None and claimed.amount.value is not None:
            fhir_claim_response.total = [claimed]

        elif valuated.amount.value is not None and reinsured.amount.value is not None and \
                approved.amount.value is None and claimed.amount.value is None:
            fhir_claim_response.total = [valuated, reinsured]

        elif valuated.amount.value is not None and reinsured.amount.value is None and \
                approved.amount.value is not None and claimed.amount.value is None:
            fhir_claim_response.total = [valuated, approved]

        elif valuated.amount.value is not None and reinsured.amount.value is None and \
                approved.amount.value is None and claimed.amount.value is not None:
            fhir_claim_response.total = [valuated, claimed]

        elif valuated.amount.value is None and reinsured.amount.value is not None and \
                approved.amount.value is not None and claimed.amount.value is None:
            fhir_claim_response.total = [reinsured, approved]

        elif valuated.amount.value is None and reinsured.amount.value is not None and \
                approved.amount.value is None and claimed.amount.value is not None:
            fhir_claim_response.total = [reinsured, claimed]

        elif valuated.amount.value is None and reinsured.amount.value is None and \
                approved.amount.value is not None and claimed.amount.value is not None:
            fhir_claim_response.total = [approved, claimed]

        elif valuated.amount.value is not None and reinsured.amount.value is not None and \
                approved.amount.value is not None and claimed.amount.value is None:
            fhir_claim_response.total = [valuated, reinsured, approved]

        elif valuated.amount.value is not None and reinsured.amount.value is not None and \
                approved.amount.value is None and claimed.amount.value is not None:
            fhir_claim_response.total = [valuated, reinsured, claimed]

        elif valuated.amount.value is None and reinsured.amount.value is not None and \
                approved.amount.value is not None and claimed.amount.value is not None:
            fhir_claim_response.total = [reinsured, approved, claimed]

        else:
            fhir_claim_response.total = [valuated, reinsured, approved, claimed]


    @classmethod
    def build_fhir_total_valuated(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.valuated is not None:
            fhir_total.category = cls.build_codeable_concept("valuated",
                                                             "http://terminology.hl7.org/CodeSystem/adjudication.html")

            fhir_total.amount.value = imis_claim.valuated
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_total_reinsured(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.reinsured is not None:
            fhir_total.category = cls.build_codeable_concept("reinsured",
                                                             "http://terminology.hl7.org/CodeSystem/adjudication.html")

            fhir_total.amount.value = imis_claim.reinsured
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_total_approved(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.approved is not None:
            fhir_total.category = cls.build_codeable_concept("approved",
                                                             "http://terminology.hl7.org/CodeSystem/adjudication.html")

            fhir_total.amount.value = imis_claim.approved
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_total_claimed(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.claimed is not None:
            fhir_total.category = cls.build_codeable_concept("claimed",
                                                             "http://terminology.hl7.org/CodeSystem/adjudication.html")

            fhir_total.amount.value = imis_claim.claimed
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_communication_request_reference(cls, fhir_claim_response, imis_claim):
        request = CommunicationRequestConverter.build_fhir_resource_reference(imis_claim)
        fhir_claim_response.communicationRequest = [request]