import os

from api_fhir.converters import CommunicationRequestConverter
from api_fhir.models import FHIRBaseObject
from api_fhir.tests import CommunicationRequestTestMixin


class CommunicationRequestConverterTestCase(CommunicationRequestTestMixin):

    __TEST_COMMUNICATION_REQUEST_JSON_PATH = "/test/test_communicationRequest.json"

    def setUp(self):
        super(CommunicationRequestConverterTestCase, self).setUp()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_claim_response_json_representation = open(dir_path + self.__TEST_COMMUNICATION_REQUEST_JSON_PATH).read()
        # .dumps() will not put a newline at the end of the "file" but editors will
        if self._test_claim_response_json_representation[-1:] == "\n":
            self._test_claim_response_json_representation = self._test_claim_response_json_representation[:-1]

    def test_to_fhir_obj(self):
        imis_feedback = self.create_test_imis_instance()
        fhir_communication_request = CommunicationRequestConverter.to_fhir_obj(imis_feedback)
        self.verify_fhir_instance(fhir_communication_request)

    def test_fhir_object_to_json_request(self):
        fhir_obj = self.create_test_fhir_instance()
        actual_representation = fhir_obj.dumps(format_='json')
        self.assertEqual(self._test_claim_response_json_representation, actual_representation)

    def test_create_object_from_json(self):
        fhir_claim = FHIRBaseObject.loads(self._test_claim_response_json_representation, 'json')
        self.verify_fhir_instance(fhir_claim)
