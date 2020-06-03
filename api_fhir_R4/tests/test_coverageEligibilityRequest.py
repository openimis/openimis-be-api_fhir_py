from coverage.annotate import os

from api_fhir_R4.converters import CoverageEligibilityRequestConverter
from api_fhir_R4.models import FHIRBaseObject
from api_fhir_R4.tests import CoverageEligibilityRequestTestMixin


class CoverageEligibilityRequestConverterTestCase(CoverageEligibilityRequestTestMixin):

    __TEST_COVERAGE_ELIGIBILITY_RESPONSE_JSON_PATH = "/test/test_coverageEligibilityResponse.json"
    __TEST_COVERAGE_ELIGIBILITY_REQUEST_JSON_PATH = "/test/test_coverageEligibilityRequest.json"

    def setUp(self):
        super(CoverageEligibilityRequestConverterTestCase, self).setUp()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_coverage_eligibility_response_json_representation = open(dir_path
                                                                   + self.__TEST_COVERAGE_ELIGIBILITY_RESPONSE_JSON_PATH) \
            .read()
        self._test_coverage_eligibility_request_json_representation = open(dir_path
                                                                  + self.__TEST_COVERAGE_ELIGIBILITY_REQUEST_JSON_PATH) \
            .read()

    def test_to_fhir_obj(self):
        imis_coverage_eligibility_response = self.create_test_imis_instance()
        fhir_coverage_eligibility_response = CoverageEligibilityRequestConverter.to_fhir_obj(imis_coverage_eligibility_response)
        self.verify_fhir_instance(fhir_coverage_eligibility_response)

    def test_to_imis_obj(self):
        fhir_coverage_eligibility_request = self.create_test_fhir_instance()
        imis_coverage_eligibility_request = CoverageEligibilityRequestConverter.to_imis_obj(fhir_coverage_eligibility_request, None)
        self.verify_imis_instance(imis_coverage_eligibility_request)

    def test_create_object_from_json(self):
        self.setUp()
        fhir_coverage_eligibility_response = FHIRBaseObject.loads(self._test_coverage_eligibility_response_json_representation,
                                                         'json')
        self.verify_fhir_instance(fhir_coverage_eligibility_response)

    def test_fhir_object_to_json_request(self):
        self.setUp()
        fhir_coverage_eligibility_request = self.create_test_fhir_instance()
        self.assertTrue(fhir_coverage_eligibility_request.patient.reference.startswith("Patient/"))
        fhir_coverage_eligibility_request.patient.reference = "Patient/chfid"
        actual_representation = fhir_coverage_eligibility_request.dumps(format_='json')
        self.assertEqual(self._test_coverage_eligibility_request_json_representation, actual_representation)

    def test_fhir_object_to_json_response(self):
        self.setUp()
        imis_coverage_eligibility_response = self.create_test_imis_instance()
        actual_representation = CoverageEligibilityRequestConverter.to_fhir_obj(imis_coverage_eligibility_response).dumps(format_='json')
        self.assertEqual(self._test_coverage_eligibility_response_json_representation, actual_representation)
