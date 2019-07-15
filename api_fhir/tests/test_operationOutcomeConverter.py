import os

from api_fhir.converters import OperationOutcomeConverter
from api_fhir.tests import OperationOutcomeTestMixin


class OperationOutcomeConverterTestCase(OperationOutcomeTestMixin):

    __TEST_OUTCOME_JSON_PATH = "/test/test_outcome.json"

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_outcome_json_representation = open(dir_path + self.__TEST_OUTCOME_JSON_PATH).read()

    def test_to_fhir_obj(self):
        exc = self.create_test_imis_instance()
        fhir_outcome = OperationOutcomeConverter.to_fhir_obj(exc)
        self.verify_fhir_instance(fhir_outcome)

    def test_fhir_object_to_json(self):
        self.setUp()
        fhir_outcome = self.create_test_fhir_instance()
        actual_representation = fhir_outcome.dumps(format_='json')
        self.assertEqual(self._test_outcome_json_representation, actual_representation)

