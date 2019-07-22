from api_fhir.configurations import Stu3IssueTypeConfig
from api_fhir.converters import BaseFHIRConverter, OperationOutcomeConverter
from api_fhir.exceptions import FHIRRequestProcessException
from api_fhir.models import IssueSeverity, CodeableConcept
from api_fhir.tests import GenericTestMixin


class OperationOutcomeTestMixin(GenericTestMixin):

    __ERROR_MESSAGE = "Error message"
    __VALID_CONDITION = 1 == 1

    def create_test_imis_instance(self):
        errors = []
        BaseFHIRConverter.valid_condition(self.__VALID_CONDITION, self.__ERROR_MESSAGE, errors)
        return FHIRRequestProcessException(errors)

    def create_test_fhir_instance(self):
        exc = self.create_test_imis_instance()
        return OperationOutcomeConverter.to_fhir_obj(exc)

    def verify_fhir_instance(self, fhir_obj):
            issues = fhir_obj.issue
            self.assertEqual(1, len(issues))
            first_issue = issues[0]
            self.assertEqual(first_issue.code, Stu3IssueTypeConfig.get_fhir_code_for_exception())
            self.assertEqual(first_issue.severity, IssueSeverity.ERROR.value)
            details = first_issue.details
            self.assertTrue(isinstance(details, CodeableConcept))
            self.assertEqual(details.text, "The request cannot be processed due to the following issues:\nError message")
