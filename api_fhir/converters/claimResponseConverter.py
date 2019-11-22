from claim.models import Feedback, ClaimItem, ClaimService
from django.db.models import Subquery
from medical.models import Item, Service

from api_fhir.configurations import Stu3ClaimConfig
from api_fhir.converters import BaseFHIRConverter, CommunicationRequestConverter
from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.exceptions import FHIRRequestProcessException
from api_fhir.models import ClaimResponse, Money, ClaimResponsePayment, ClaimResponseError, ClaimResponseItem, Claim, \
    ClaimResponseItemAdjudication, ClaimResponseProcessNote, ClaimResponseAddItem
from api_fhir.utils import TimeUtils, FhirUtils


class ClaimResponseConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim):
        fhir_claim_response = ClaimResponse()
        fhir_claim_response.created = TimeUtils.date().isoformat()
        fhir_claim_response.request = ClaimConverter.build_fhir_resource_reference(imis_claim)
        cls.build_fhir_pk(fhir_claim_response, imis_claim.uuid)
        ClaimConverter.build_fhir_identifiers(fhir_claim_response, imis_claim)
        cls.build_fhir_outcome(fhir_claim_response, imis_claim)
        cls.build_fhir_payment(fhir_claim_response, imis_claim)
        cls.build_fhir_total_benefit(fhir_claim_response, imis_claim)
        cls.build_fhir_errors(fhir_claim_response, imis_claim)
        cls.build_fhir_communication_request_reference(fhir_claim_response, imis_claim)
        cls.build_fhir_items(fhir_claim_response, imis_claim)
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
            display = Stu3ClaimConfig.get_fhir_claim_status_rejected_code()
        elif code == 2:
            display = Stu3ClaimConfig.get_fhir_claim_status_entered_code()
        elif code == 4:
            display = Stu3ClaimConfig.get_fhir_claim_status_checked_code()
        elif code == 8:
            display = Stu3ClaimConfig.get_fhir_claim_status_processed_code()
        elif code == 16:
            display = Stu3ClaimConfig.get_fhir_claim_status_valuated_code()
        return display

    @classmethod
    def build_fhir_payment(cls, fhir_claim_response, imis_claim):
        fhir_payment = ClaimResponsePayment()
        fhir_payment.adjustmentReason = cls.build_simple_codeable_concept(imis_claim.adjustment)
        date_processed = imis_claim.date_processed
        if date_processed:
            fhir_payment.date = date_processed.isoformat()
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
            fhir_error.code = cls.build_codeable_concept(str(rejection_reason))
            fhir_claim_response.error = [fhir_error]

    @classmethod
    def build_fhir_communication_request_reference(cls, fhir_claim_response, imis_claim):
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
            code = claim_item.service.text

            if type == Stu3ClaimConfig.get_fhir_claim_item_code():
                serviced = cls.get_imis_claim_item_by_code(code, imis_claim.id)
            elif  type == Stu3ClaimConfig.get_fhir_claim_service_code():
                serviced = cls.get_service_claim_item_by_code(code, imis_claim.id)
            else:
                raise FHIRRequestProcessException(['Could not assign category {} for claim_item: {}'
                                                  .format(type, claim_item)])

            cls._build_response_items(fhir_claim_response, claim_item, serviced, serviced.rejection_reason)

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
        item_code = claim_item.service.text
        add_item.sequenceLinkId.append(claim_item.sequence)
        add_item.service = cls.build_codeable_concept(code=item_code)
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
        claim_response_item.sequenceLinkId = claim_item.sequence
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
            cls.build_simple_codeable_concept(Stu3ClaimConfig.get_fhir_claim_item_general_adjudication_code())
        item_adjudication.reason = cls.build_fhir_adjudication_reason(item)
        item_adjudication.value = item.qty_approved
        limitation_value = Money()
        limitation_value.value = item.limitation_value
        item_adjudication.amount = limitation_value
        claim_response_item.adjudication.append(item_adjudication)

    @classmethod
    def build_fhir_item_rejected_reason_adjudication(cls, claim_response_item, rejection_reason):
        item_adjudication = ClaimResponseItemAdjudication()
        item_adjudication.category = \
            cls.build_simple_codeable_concept(Stu3ClaimConfig.get_fhir_claim_item_rejected_reason_adjudication_code())
        item_adjudication.reason = cls.build_codeable_concept(rejection_reason)
        claim_response_item.adjudication.append(item_adjudication)

    @classmethod
    def build_fhir_adjudication_reason(cls, item):
        status = item.status
        text_code = None
        if status == 1:
            text_code = Stu3ClaimConfig.get_fhir_claim_item_status_passed_code()
        elif status == 2:
            text_code = Stu3ClaimConfig.get_fhir_claim_item_status_rejected_code()
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
