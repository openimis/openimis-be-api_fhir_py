from enum import Enum

from api_fhir.models import DomainResource, Property, BackboneElement


class IssueSeverity(Enum):
    FATAL = "fatal"
    ERROR = "error"
    WARNING = "warning"
    INFORMATION = "information"


class OperationOutcomeIssue(BackboneElement):

    severity = Property('severity', str, required=True)
    code = Property('code', str, required=True)
    details = Property('details', 'CodeableConcept')
    diagnostics = Property('diagnostics', str)
    location = Property('location', str, count_max='*')
    expression = Property('expression', str, count_max='*')


class OperationOutcome(DomainResource):

    issue = Property('issue', 'OperationOutcomeIssue', count_max='*')
