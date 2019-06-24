from api_fhir.configurations import Stu3IssueTypeConfig
from api_fhir.converters import BaseFHIRConverter
from api_fhir.exceptions import FHIRException
from api_fhir.models import OperationOutcome, OperationOutcomeIssue
from api_fhir.models.operationOutcome import IssueSeverity


class OperationOutcomeConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, obj):
        if isinstance(obj, FHIRException):
            return cls.build_exception_outcome(obj)

    @classmethod
    def to_imis_obj(cls, data, audit_user_id):
        raise NotImplementedError('`toImisObj()` must be implemented.')

    @classmethod
    def build_exception_outcome(cls, obj):
        outcome = OperationOutcome()
        if isinstance(obj, FHIRException):
            issue = OperationOutcomeIssue()
            issue.severity = IssueSeverity.ERROR.value
            issue.code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
            issue.details = cls.build_simple_codeable_concept(text=obj.detail)
            outcome.issue.append(issue)
        return outcome
