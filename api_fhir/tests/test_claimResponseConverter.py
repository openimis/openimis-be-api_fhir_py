import os
from unittest import mock

from api_fhir.converters import ClaimResponseConverter
from api_fhir.models import FHIRBaseObject
from api_fhir.tests import ClaimResponseTestMixin


class ClaimResponseConverterTestCase(ClaimResponseTestMixin):

    __TEST_CLAIM_RESPONSE_JSON_PATH = "/test/test_claimResponse.json"

    def setUp(self):
        super(ClaimResponseConverterTestCase, self).setUp()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_claim_response_json_representation = open(dir_path + self.__TEST_CLAIM_RESPONSE_JSON_PATH).read()
        if self._test_claim_response_json_representation[-1:] == "\n":
            self._test_claim_response_json_representation = self._test_claim_response_json_representation[:-1]


    @mock.patch('claim.models.ClaimItem.objects')
    @mock.patch('claim.models.ClaimService.objects')
    def test_to_fhir_obj(self, cs_mock, ci_mock):
        cs_mock.filter.return_value = [self._TEST_SERVICE]
        ci_mock.filter.return_value = [self._TEST_ITEM]

        imis_claim_response = self.create_test_imis_instance()
        fhir_claim_response = ClaimResponseConverter.to_fhir_obj(imis_claim_response)
        self.verify_fhir_instance(fhir_claim_response)

    def test_fhir_object_to_json_request(self):
        fhir_obj = self.create_test_fhir_instance()
        actual_representation = fhir_obj.dumps(format_='json')
        self.assertEqual(self._test_claim_response_json_representation, actual_representation)

    def test_create_object_from_json(self):
        fhir_claim = FHIRBaseObject.loads(self._test_claim_response_json_representation, 'json')
        self.verify_fhir_instance(fhir_claim)
