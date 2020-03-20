from claim.models import Feedback

from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.converters import CommunicationRequestConverter as Converter
from api_fhir.configurations import Stu3CommunicationRequestConfig as Config
from api_fhir.models import CommunicationRequest
from api_fhir.tests import GenericTestMixin
from api_fhir.utils import TimeUtils


class CommunicationRequestTestMixin(GenericTestMixin):

    _TEST_FEEDBACK_ID = "1"
    _TEST_FEEDBACK_UUID = "612a1e12-ce44-4632-90a8-129ec714ec59"
    _TEST_FEEDBACK_DATE = "2010-11-16T00:00:00"
    _TEST_CARE_RENDERED = True
    _TEST_PAYMENT_ASKED = False
    _TEST_DRUG_PRESCRIBED = True
    _TEST_DRUG_RECEIVED = False
    _TEST_ASESSMENT = 2

    def create_test_imis_instance(self):
        imis_feedback = Feedback()
        imis_feedback.id = self._TEST_FEEDBACK_ID
        imis_feedback.uuid = self._TEST_FEEDBACK_UUID
        imis_feedback.feedback_date = TimeUtils.str_to_date(self._TEST_FEEDBACK_DATE)
        imis_feedback.care_rendered = self._TEST_CARE_RENDERED
        imis_feedback.payment_asked = self._TEST_PAYMENT_ASKED
        imis_feedback.drug_prescribed = self._TEST_DRUG_PRESCRIBED
        imis_feedback.drug_received = self._TEST_DRUG_RECEIVED
        imis_feedback.asessment = self._TEST_ASESSMENT
        return imis_feedback

    def create_test_fhir_instance(self):
        fhir_communication_request = CommunicationRequest()
        fhir_communication_request.id = self._TEST_FEEDBACK_UUID
        fhir_communication_request.occurrenceDateTime = self._TEST_FEEDBACK_DATE
        identifiers = []
        identifier = Converter.build_fhir_identifier(self._TEST_FEEDBACK_UUID,
                                                     Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                     Stu3IdentifierConfig.get_fhir_uuid_type_code())
        identifiers.append(identifier)
        fhir_communication_request.identifier = identifiers
        reasons = [Converter.build_codeable_concept(Config.get_fhir_care_rendered_code(),
                                                    text=str(self._TEST_CARE_RENDERED)),
                   Converter.build_codeable_concept(Config.get_fhir_payment_asked_code(),
                                                    text=str(self._TEST_PAYMENT_ASKED)),
                   Converter.build_codeable_concept(Config.get_fhir_drug_prescribed_code(),
                                                    text=str(self._TEST_DRUG_PRESCRIBED)),
                   Converter.build_codeable_concept(Config.get_fhir_drug_received_code(),
                                                    text=str(self._TEST_DRUG_RECEIVED)),
                   Converter.build_codeable_concept(Config.get_fhir_asessment_code(),
                                                    text=str(self._TEST_ASESSMENT))]
        fhir_communication_request.reasonCode = reasons
        return fhir_communication_request

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(self._TEST_FEEDBACK_UUID, fhir_obj.id)
        self.assertEqual(self._TEST_FEEDBACK_UUID, fhir_obj.identifier[0].value)
        self.assertEqual(self._TEST_FEEDBACK_DATE, fhir_obj.occurrenceDateTime)
        for reason in fhir_obj.reasonCode:
            value = reason.text
            code = reason.coding[0].code
            if code == Config.get_fhir_care_rendered_code():
                self.assertEqual(str(self._TEST_CARE_RENDERED), value)
            elif code == Config.get_fhir_payment_asked_code():
                self.assertEqual(str(self._TEST_PAYMENT_ASKED), value)
            elif code == Config.get_fhir_drug_prescribed_code():
                self.assertEqual(str(self._TEST_DRUG_PRESCRIBED), value)
            elif code == Config.get_fhir_drug_received_code():
                self.assertEqual(str(self._TEST_DRUG_RECEIVED), value)
            elif code == Config.get_fhir_asessment_code():
                self.assertEqual(str(self._TEST_ASESSMENT), value)
