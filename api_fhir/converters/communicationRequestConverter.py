from claim.models import Feedback

from api_fhir.converters import BaseFHIRConverter, ReferenceConverterMixin
from api_fhir.models.communicationRequest import CommunicationRequest


class CommunicationRequestConverter(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_feedback):
        fhir_communication_request = CommunicationRequest()
        cls.build_fhir_pk(fhir_communication_request, imis_feedback.id)
        return fhir_communication_request

    @classmethod
    def get_reference_obj_id(cls, imis_feedback):
        return imis_feedback.id

    @classmethod
    def get_fhir_resource_type(cls):
        return CommunicationRequest

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_feedback_id = cls.get_resource_id_from_reference(reference)
        return Feedback.objects.filter(pk=imis_feedback_id).first()
