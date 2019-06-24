from api_fhir.configurations import ModuleConfiguration
from api_fhir.exceptions import FHIRException
from api_fhir.utils import FunctionUtils

from rest_framework.views import exception_handler


def call_default_exception_handler(exc, context):
    response = None
    handler = ModuleConfiguration.get_default_api_error_handler()
    if handler:
        # Call default exception handler which can be defined in separate IMIS handler
        func = FunctionUtils.get_function_by_str(handler)
        if func:
            response = func(exc, context)
    else:
        # Call REST framework's default exception handler first, to get the standard error response.
        response = exception_handler(exc, context)
    return response


def fhir_api_exception_handler(exc, context):
    response = call_default_exception_handler(exc, context)

    if response and isinstance(exc, FHIRException):
        from api_fhir.converters import OperationOutcomeConverter
        fhir_outcome = OperationOutcomeConverter.to_fhir_obj(exc)
        response.data = fhir_outcome.toDict()

    return response
