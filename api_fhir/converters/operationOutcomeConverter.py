from django.http import Http404

from api_fhir.configurations import Stu3IssueTypeConfig
from api_fhir.converters import BaseFHIRConverter
from api_fhir.exceptions import FHIRException
from api_fhir.models import OperationOutcome, OperationOutcomeIssue
from api_fhir.models.operationOutcome import IssueSeverity


class OperationOutcomeConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, obj):
        result = OperationOutcome()
        if isinstance(obj, FHIRException):
            result = cls.build_for_fhir_exception(obj)
        elif isinstance(obj, Http404):
            result = cls.build_for_404()
        elif isinstance(obj, KeyError):
            result = cls.build_for_key_error(obj)
        elif isinstance(obj, Exception):
            result = cls.build_for_generic_error(obj)
        return result

    @classmethod
    def build_for_fhir_exception(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = obj.detail
        return cls.build_exception_outcome(severity, code, details_text)

    @classmethod
    def build_for_404(cls):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_not_found()
        return cls.build_exception_outcome(severity, code)

    @classmethod
    def build_for_key_error(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = cls.get_first_message_from_generic_exception(obj) + ' is missing'
        return cls.build_exception_outcome(severity, code, details_text)

    @classmethod
    def build_for_generic_error(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = cls.get_first_message_from_generic_exception(obj)
        return cls.build_exception_outcome(severity, code, details_text)

    @classmethod
    def get_first_message_from_generic_exception(cls, obj):
        return obj.args[0]

    @classmethod
    def build_exception_outcome(cls, severity, code, details_text=None):
        outcome = OperationOutcome()
        issue = OperationOutcomeIssue()
        issue.severity = severity
        issue.code = code
        if details_text:
            issue.details = cls.build_simple_codeable_concept(text=details_text)
        outcome.issue.append(issue)
        return outcome
