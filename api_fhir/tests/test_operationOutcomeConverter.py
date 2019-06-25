import os
from unittest import TestCase

from api_fhir.configurations import Stu3IssueTypeConfig
from api_fhir.converters import OperationOutcomeConverter, BaseFHIRConverter
from api_fhir.exceptions import FHIRRequestProcessException
from api_fhir.models import FHIRBaseObject, CodeableConcept, IssueSeverity


class OperationOutcomeConverterTestCase(TestCase):

    __ERROR_MESSAGE = "Error message"
    __VALID_CONDITION = 1 == 1
    __TEST_OUTCOME_JSON_PATH = "/test/test_outcome.json"

    def __set_up(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_outcome_json_representation = open(dir_path + self.__TEST_OUTCOME_JSON_PATH).read()

    def test_to_fhir_obj(self):
        exc = self.create_test_fhir_request_process_exception()
        fhir_outcome = OperationOutcomeConverter.to_fhir_obj(exc)
        self.verify_fhir_outcome(fhir_outcome)

    def test_fhir_object_to_json(self):
        self.__set_up()
        fhir_outcome = self.create_fhir_outcome_test_instance()
        actual_representation = FHIRBaseObject.dumps(fhir_outcome, 'json')
        self.assertEqual(self._test_outcome_json_representation, actual_representation)

    def create_fhir_outcome_test_instance(self):
        exc = self.create_test_fhir_request_process_exception()
        return OperationOutcomeConverter.to_fhir_obj(exc)

    def create_test_fhir_request_process_exception(self):
        errors = []
        BaseFHIRConverter.valid_condition(self.__VALID_CONDITION, self.__ERROR_MESSAGE, errors)
        return FHIRRequestProcessException(errors)

    def verify_fhir_outcome(self, fhir_outcome):
        issues = fhir_outcome.issue
        self.assertEqual(1, len(issues))
        firstIssue = issues[0]
        self.assertEqual(firstIssue.code, Stu3IssueTypeConfig.get_fhir_code_for_exception())
        self.assertEqual(firstIssue.severity, IssueSeverity.ERROR.value)
        details = firstIssue.details
        self.assertTrue(isinstance(details, CodeableConcept))
        self.assertEqual(details.text, "The request cannot be processed due to the following issues:\nError message")

