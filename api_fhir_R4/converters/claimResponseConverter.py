from claim.models import Feedback, ClaimItem, ClaimService
from django.db.models import Subquery
from medical.models import Item, Service
import core

from api_fhir_R4.configurations import R4ClaimConfig
from api_fhir_R4.converters import BaseFHIRConverter, CommunicationRequestConverter
from api_fhir_R4.converters.claimConverter import ClaimConverter
from api_fhir_R4.converters.patientConverter import PatientConverter
from api_fhir_R4.converters.healthcareServiceConverter import HealthcareServiceConverter
from api_fhir_R4.converters.activityDefinitionConverter import ActivityDefinitionConverter
from api_fhir_R4.converters.medicationConverter import MedicationConverter
from api_fhir_R4.exceptions import FHIRRequestProcessException
from api_fhir_R4.models import ClaimResponse, Money, ClaimResponsePayment, ClaimResponseError, ClaimResponseItem, Claim, \
    ClaimResponseItemAdjudication, ClaimResponseProcessNote, ClaimResponseAddItem, ClaimResponseTotal, CodeableConcept, \
    Coding, Reference, Extension
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
        cls.build_fhir_type(fhir_claim_response, imis_claim)
        cls.build_fhir_status(fhir_claim_response)
        cls.build_fhir_use(fhir_claim_response)
        cls.build_fhir_insurer(fhir_claim_response, imis_claim)
        #cls.build_fhir_item(fhir_claim_response, imis_claim)
        return fhir_claim_response

    @classmethod
    def build_fhir_outcome(cls, fhir_claim_response, imis_claim):
        code = imis_claim.status
        if code is not None:
            display = cls.get_status_display_by_code(code)
            #fhir_claim_response.outcome = cls.build_codeable_concept(str(code), system=None, text=display)
            fhir_claim_response.outcome = display

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

    # @classmethod
    # def build_fhir_items(cls, fhir_claim_response, imis_claim):
    #     for claim_item in cls.generate_fhir_claim_items(imis_claim):
    #         type = claim_item.category.text
    #         code = claim_item.productOrService.text
    #
    #         if type == R4ClaimConfig.get_fhir_claim_item_code():
    #             serviced = cls.get_imis_claim_item_by_code(code, imis_claim.id)
    #         elif type == R4ClaimConfig.get_fhir_claim_service_code():
    #             serviced = cls.get_service_claim_item_by_code(code, imis_claim.id)
    #         else:
    #             raise FHIRRequestProcessException(['Could not assign category {} for claim_item: {}'
    #                                               .format(type, claim_item)])
    #
    #         cls._build_response_items(fhir_claim_response, claim_item, serviced, serviced.rejection_reason)
    #
    # @classmethod
    # def _build_response_items(cls, fhir_claim_response, claim_item, imis_service, rejected_reason):
    #     cls.build_fhir_item(fhir_claim_response, claim_item, imis_service,
    #                         rejected_reason=rejected_reason)
    #     #cls.build_fhir_claim_add_item(fhir_claim_response, claim_item)
    #
    # @classmethod
    # def generate_fhir_claim_items(cls, imis_claim):
    #     claim = Claim()
    #     ClaimConverter.build_fhir_items(claim, imis_claim)
    #     return claim.item
    #
    # @classmethod
    # def get_imis_claim_item_by_code(cls, code, imis_claim_id):
    #     item_code_qs = Item.objects.filter(code=code)
    #     result = ClaimItem.objects.filter(item_id__in=Subquery(item_code_qs.values('id')), claim_id=imis_claim_id)
    #     return result[0] if len(result) > 0 else None
    #
    # @classmethod
    # def build_fhir_claim_add_item(cls, fhir_claim_response, claim_item):
    #     add_item = ClaimResponseAddItem()
    #     item_code = claim_item.productOrService.text
    #     add_item.itemSequence.append(claim_item.sequence)
    #     add_item.productOrService = cls.build_codeable_concept(code=item_code)
    #     fhir_claim_response.addItem.append(add_item)
    #
    # @classmethod
    # def get_service_claim_item_by_code(cls, code, imis_claim_id):
    #     service_code_qs = Service.objects.filter(code=code)
    #     result = ClaimService.objects.filter(service_id__in=Subquery(service_code_qs.values('id')),
    #                                          claim_id=imis_claim_id)
    #     return result[0] if len(result) > 0 else None
    #
    # @classmethod
    # def build_fhir_item(cls, fhir_claim_response, claim_item, item, rejected_reason=None):
    #     claim_response_item = ClaimResponseItem()
    #     claim_response_item.itemSequence = claim_item.sequence
    #     cls.build_fhir_item_general_adjudication(claim_response_item, item)
    #     if rejected_reason:
    #         cls.build_fhir_item_rejected_reason_adjudication(claim_response_item, rejected_reason)
    #     note = cls.build_process_note(fhir_claim_response, item.justification)
    #     if note:
    #         claim_response_item.noteNumber = [note.number]
    #     fhir_claim_response.item.append(claim_response_item)
    #
    # @classmethod
    # def build_fhir_item_general_adjudication(cls, claim_response_item, item):
    #     item_adjudication = ClaimResponseItemAdjudication()
    #     item_adjudication.category = \
    #         cls.build_simple_codeable_concept(R4ClaimConfig.get_fhir_claim_item_general_adjudication_code())
    #     item_adjudication.reason = cls.build_fhir_adjudication_reason(item)
    #     item_adjudication.value = item.qty_approved
    #     price_valuated = Money()
    #     price_valuated.value = item.price_valuated
    #     item_adjudication.amount = price_valuated
    #     claim_response_item.adjudication.append(item_adjudication)
    #
    # @classmethod
    # def build_fhir_item_rejected_reason_adjudication(cls, claim_response_item, rejection_reason):
    #     item_adjudication = ClaimResponseItemAdjudication()
    #     item_adjudication.category = \
    #         cls.build_simple_codeable_concept(R4ClaimConfig.get_fhir_claim_item_rejected_reason_adjudication_code())
    #     item_adjudication.reason = cls.build_codeable_concept(rejection_reason)
    #     claim_response_item.adjudication.append(item_adjudication)
    #
    # @classmethod
    # def build_fhir_adjudication_reason(cls, item):
    #     status = item.status
    #     text_code = None
    #     if status == 1:
    #         text_code = R4ClaimConfig.get_fhir_claim_item_status_passed_code()
    #     elif status == 2:
    #         text_code = R4ClaimConfig.get_fhir_claim_item_status_rejected_code()
    #     return cls.build_codeable_concept(status, text=text_code)

    # @classmethod
    # def build_process_note(cls, fhir_claim_response, string_value):
    #     result = None
    #     if string_value:
    #         note = ClaimResponseProcessNote()
    #         note.number = FhirUtils.get_next_array_sequential_id(fhir_claim_response.processNote)
    #         note.text = string_value
    #         fhir_claim_response.processNote.append(note)
    #         result = note
    #     return result

    @classmethod
    def build_patient_reference(cls, fhir_claim_response, imis_claim):
        fhir_claim_response.patient = PatientConverter.build_fhir_resource_reference(imis_claim.insuree)

    @classmethod
    def build_fhir_total(cls, fhir_claim_response, imis_claim):
        valuated = cls.build_fhir_total_valuated(imis_claim)
        reinsured = cls.build_fhir_total_reinsured(imis_claim)
        approved = cls.build_fhir_total_approved(imis_claim)
        claimed = cls.build_fhir_total_claimed(imis_claim)

        if valuated.amount.value is None and reinsured.amount.value is None and \
                approved.amount.value is None and claimed.amount.value is not None:
            fhir_claim_response.total = [claimed]

        elif valuated.amount.value is None and reinsured.amount.value is None and \
                approved.amount.value is not None and claimed.amount.value is not None:
            fhir_claim_response.total = [approved, claimed]

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

            fhir_total.category = CodeableConcept()
            coding = Coding()
            coding.code = "V"
            coding.system = "http://terminology.hl7.org/CodeSystem/adjudication.html"
            coding.display = "Valuated"
            fhir_total.category.coding.append(coding)
            fhir_total.category.text = "Valuated < Reinsured < Approved < Claimed"

            fhir_total.amount.value = imis_claim.valuated
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_total_reinsured(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.reinsured is not None:
            fhir_total.category = CodeableConcept()
            coding = Coding()
            coding.code = "R"
            coding.system = "http://terminology.hl7.org/CodeSystem/adjudication.html"
            coding.display = "Reinsured"
            fhir_total.category.coding.append(coding)
            fhir_total.category.text = "Valuated < Reinsured < Approved < Claimed"


            fhir_total.amount.value = imis_claim.reinsured
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_total_approved(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.approved is not None:

            fhir_total.category = CodeableConcept()
            coding = Coding()
            coding.code = "A"
            coding.system = "http://terminology.hl7.org/CodeSystem/adjudication.html"
            coding.display = "Approved"
            fhir_total.category.coding.append(coding)
            fhir_total.category.text = "Valuated < Reinsured < Approved < Claimed"

            fhir_total.amount.value = imis_claim.approved
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_total_claimed(cls, imis_claim):
        fhir_total = ClaimResponseTotal()
        money = Money()
        fhir_total.amount = money

        if imis_claim.claimed is not None:

            fhir_total.category = CodeableConcept()
            coding = Coding()
            coding.code = "C"
            coding.system = "http://terminology.hl7.org/CodeSystem/adjudication.html"
            coding.display = "Claimed"
            fhir_total.category.coding.append(coding)
            fhir_total.category.text = "Valuated < Reinsured < Approved < Claimed"

            fhir_total.amount.value = imis_claim.claimed
            fhir_total.amount.currency = core.currency

        return fhir_total

    @classmethod
    def build_fhir_communication_request_reference(cls, fhir_claim_response, imis_claim):
        request = CommunicationRequestConverter.build_fhir_resource_reference(imis_claim)
        fhir_claim_response.communicationRequest = [request]

    @classmethod
    def build_fhir_type(cls, fhir_claim_response, imis_claim):
        if imis_claim.visit_type:
            fhir_claim_response.type = cls.build_simple_codeable_concept(imis_claim.visit_type)

    @classmethod
    def build_fhir_status(cls, fhir_claim_response):
        if fhir_claim_response.outcome == "entered":
            fhir_claim_response.status = "draft"
        elif fhir_claim_response.outcome == "valuated":
            fhir_claim_response.status = "completed"
        elif fhir_claim_response.outcome == "rejected":
            fhir_claim_response.status = "entered-in-error"
        else:
            fhir_claim_response.status = "active"

    @classmethod
    def build_fhir_use(cls, fhir_claim_response):
        fhir_claim_response.use = "claim"

    @classmethod
    def build_fhir_insurer(cls, fhir_claim_response, imis_claim):
        fhir_claim_response.insurer = HealthcareServiceConverter.build_fhir_resource_reference(
            imis_claim.health_facility)

    """
    @classmethod
    def build_fhir_item(cls, fhir_claim_response, imis_claim):
        fhir_item = ClaimResponseItem()
        fhir_item.itemSequence = 0

    @classmethod
    def build_fhir_adjudication(cls, imis_claim):
        fhir_adjudication = ClaimResponseItemAdjudication()

    @classmethod
    def build_fhir_adjudication_reason(cls, imis_claim):
        category = CodeableConcept()
        reason = CodeableConcept()
        reason = cls.build_codeable_concept()
    """





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

            cls._build_response_items(fhir_claim_response, claim_item, serviced, type, serviced.rejection_reason, imis_claim)

    @classmethod
    def _build_response_items(cls, fhir_claim_response, claim_item, imis_service, type, rejected_reason, imis_claim):
        cls.build_fhir_item(fhir_claim_response, claim_item, imis_service, type, rejected_reason, imis_claim)

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
    def get_service_claim_item_by_code(cls, code, imis_claim_id):
        service_code_qs = Service.objects.filter(code=code)
        result = ClaimService.objects.filter(service_id__in=Subquery(service_code_qs.values('id')),
                                             claim_id=imis_claim_id)
        return result[0] if len(result) > 0 else None

    @classmethod
    def build_fhir_item(cls, fhir_claim_response, claim_item, item, type, rejected_reason, imis_claim):
        claim_response_item = ClaimResponseItem()
        claim_response_item.itemSequence = claim_item.sequence

        adjudication = cls.build_fhir_item_adjudication(item, rejected_reason, imis_claim)
        claim_response_item.adjudication = adjudication

        extension = Extension()

        if type == "item":
            medication = cls.build_medication_extension(extension)
            claim_response_item.extension.append(medication)

        elif type == "service":
            activity_definition = cls.build_activity_definition_extension(extension)
            claim_response_item.extension.append(activity_definition)

        note = cls.build_process_note(fhir_claim_response, item.price_origin)
        if note:
            claim_response_item.noteNumber = [note.number]
        fhir_claim_response.item.append(claim_response_item)

    @classmethod
    def build_medication_extension(cls, extension):
        imis_item = ClaimItem()
        reference = Reference()
        extension.valueReference = reference
        extension.url = "Medication"
        imis_item.item = Item()
        extension.valueReference = MedicationConverter.build_fhir_resource_reference(imis_item.item)
        return extension

    @classmethod
    def build_activity_definition_extension(cls, extension):
        imis_service = ClaimService()
        reference = Reference()
        extension.valueReference = reference
        extension.url = "ActivityDefinition"
        imis_service.service = Service()
        extension.valueReference = ActivityDefinitionConverter.build_fhir_resource_reference(imis_service.service)
        return extension

    # @classmethod
    # def build_fhir_item_adjudication(cls, item, rejected_reason, imis_claim):
    #     item_adjudication = ClaimResponseItemAdjudication()
    #
    #     text = ""
    #     if imis_claim.status == 1:
    #         text = "rejected"
    #     if imis_claim.status == 2:
    #         text = "entered"
    #     if imis_claim.status == 4:
    #         text = "checked"
    #     if imis_claim.status == 8:
    #         text = "processed"
    #     if imis_claim.status == 16:
    #         text = "valuated"
    #
    #     item_adjudication.category = \
    #         cls.build_codeable_concept(imis_claim.status, text=text)
    #     item_adjudication.reason = cls.build_fhir_adjudication_reason(item, rejected_reason)
    #
    #     price = Money()
    #     value = None
    #
    #     if item.price_asked is not None:
    #         if item.price_asked != 0.0:
    #             price.value = item.price_asked
    #
    #     if item.price_adjusted is not None:
    #         if item.price_adjusted != 0.0:
    #             price.value = item.price_adjusted
    #
    #     if item.price_approved is not None:
    #         if item.price_approved != 0.0:
    #             price.value = item.price_approved
    #
    #     if item.price_valuated is not None:
    #         if item.price_valuated != 0.0:
    #             price.value = item.price_valuated
    #
    #     item_adjudication.amount = price
    #
    #     if rejected_reason == 0:
    #         value = item.qty_approved
    #     else:
    #         value = item.qty_provided
    #
    #     item_adjudication.value = value
    #
    #     return [item_adjudication, item_adjudication]

    @classmethod
    def build_fhir_item_adjudication(cls, item, rejected_reason, imis_claim):
        item_adjudication_asked = ClaimResponseItemAdjudication()
        item_adjudication_adjusted = ClaimResponseItemAdjudication()
        item_adjudication_approved = ClaimResponseItemAdjudication()
        item_adjudication_valuated = ClaimResponseItemAdjudication()

        price_asked = Money()
        price_asked.currency = core.currency
        price_asked.value = item.price_asked
        price_adjusted = Money()
        price_adjusted.currency = core.currency
        price_adjusted.value = item.price_adjusted
        price_approved = Money()
        price_approved.currency = core.currency
        price_approved.value = item.price_approved
        price_valuated = Money()
        price_valuated.currency = core.currency
        price_valuated.value = item.price_valuated
        value = None

        if rejected_reason == 0:
            value = item.qty_approved
        else:
            value = item.qty_provided

        item_adjudication_asked.reason = cls.build_fhir_adjudication_reason(item, rejected_reason)
        item_adjudication_asked.amount = price_asked
        item_adjudication_asked.value = value

        item_adjudication_adjusted.reason = cls.build_fhir_adjudication_reason(item, rejected_reason)
        item_adjudication_adjusted.amount = price_adjusted
        item_adjudication_adjusted.value = value

        item_adjudication_approved.reason = cls.build_fhir_adjudication_reason(item, rejected_reason)
        item_adjudication_approved.amount = price_approved
        item_adjudication_approved.value = value

        item_adjudication_valuated.reason = cls.build_fhir_adjudication_reason(item, rejected_reason)
        item_adjudication_valuated.amount = price_valuated
        item_adjudication_valuated.value = value

        if imis_claim.status == 1:

            item_adjudication_asked.category = \
                cls.build_codeable_concept(imis_claim.status, text="rejected")

            return [item_adjudication_asked]

        if imis_claim.status == 2:

            item_adjudication_asked.category = \
                cls.build_codeable_concept(imis_claim.status, text="entered")

            return [item_adjudication_asked]

        if imis_claim.status == 4:

            item_adjudication_asked.category = \
                cls.build_codeable_concept(imis_claim.status, text="checked")
            item_adjudication_adjusted.category = \
                cls.build_codeable_concept(imis_claim.status, text="checked")

            return [item_adjudication_asked, item_adjudication_adjusted]

        if imis_claim.status == 8:

            item_adjudication_asked.category = \
                cls.build_codeable_concept(imis_claim.status, text="processed")
            item_adjudication_adjusted.category = \
                cls.build_codeable_concept(imis_claim.status, text="processed")
            item_adjudication_approved.category = \
                cls.build_codeable_concept(imis_claim.status, text="processed")

            return [item_adjudication_asked, item_adjudication_adjusted, item_adjudication_approved]

        if imis_claim.status == 16:

            item_adjudication_asked.category = \
                cls.build_codeable_concept(imis_claim.status, text="valuated")
            item_adjudication_adjusted.category = \
                cls.build_codeable_concept(imis_claim.status, text="valuated")
            item_adjudication_approved.category = \
                cls.build_codeable_concept(imis_claim.status, text="valuated")
            item_adjudication_valuated.category = \
                cls.build_codeable_concept(imis_claim.status, text="valuated")

            return [item_adjudication_asked, item_adjudication_adjusted, item_adjudication_approved, item_adjudication_valuated]

    @classmethod
    def build_fhir_adjudication_reason(cls, item, rejected_reason):
        text = None
        code = None
        if item.justification is not None:
            text = item.justification
        if rejected_reason == 0:
            code = "0"
        else:
            code = rejected_reason

        return cls.build_codeable_concept(code, text=text)

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
