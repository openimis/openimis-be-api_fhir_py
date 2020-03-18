from claim import ClaimSubmitError
from django.db import IntegrityError
from django.http import Http404
from django.http.response import HttpResponse
from rest_framework.exceptions import APIException

from api_fhir.configurations import Stu3IssueTypeConfig
from api_fhir.converters import BaseFHIRConverter
from api_fhir.exceptions import FHIRException
from api_fhir.models import OperationOutcome, OperationOutcomeIssue
from api_fhir.models.operationOutcome import IssueSeverity


class OperationOutcomeConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, obj):
        result = OperationOutcome()
        if isinstance(obj, HttpResponse):
            result = cls.build_for_http_response(obj)
        elif isinstance(obj, Exception):
            result = cls.build_for_exception(obj)
        return result

    @classmethod
    def build_for_http_response(cls, obj):
        severity = IssueSeverity.INFORMATION.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_informational()
        details_text = obj.content.decode("utf-8")
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_for_exception(cls, obj):
        result = None
        if isinstance(obj, FHIRException):
            result = cls.build_for_fhir_exception(obj)
        elif isinstance(obj, ClaimSubmitError):
            result = cls.build_for_fhir_claim_submit_error(obj)
        elif isinstance(obj, Http404):
            result = cls.build_for_404()
        elif isinstance(obj, APIException):
            result = cls.build_for_key_api_exception(obj)
        elif isinstance(obj, KeyError):
            result = cls.build_for_key_error(obj)
        elif isinstance(obj, IntegrityError):
            result = cls.build_for_IntegrityError(obj)
        else:
            result = cls.build_for_generic_error(obj)
        return result

    @classmethod
    def build_for_fhir_exception(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = obj.detail
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_for_404(cls):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_not_found()
        return cls.build_outcome(severity, code)

    @classmethod
    def build_for_400_bad_request(cls, details_text=None):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_for_key_error(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = cls.get_last_message(obj) + ' is missing'
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_for_generic_error(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = cls.get_last_message(obj)
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def get_last_message(cls, obj):
        return obj.args[len(obj.args) - 1]

    @classmethod
    def build_for_key_api_exception(cls, obj):
        severity = IssueSeverity.FATAL.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = obj.detail
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_for_fhir_claim_submit_error(cls, obj):
        severity = IssueSeverity.ERROR.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = obj.msg
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_for_IntegrityError(cls, obj):
        severity = IssueSeverity.FATAL.value
        code = Stu3IssueTypeConfig.get_fhir_code_for_exception()
        details_text = obj.args[1]
        return cls.build_outcome(severity, code, details_text)

    @classmethod
    def build_outcome(cls, severity, code, details_text=None):
        outcome = OperationOutcome()
        issue = OperationOutcomeIssue()
        issue.severity = severity
        issue.code = code
        if details_text:
            issue.details = cls.build_simple_codeable_concept(text=details_text)
        outcome.issue.append(issue)
        return outcome
