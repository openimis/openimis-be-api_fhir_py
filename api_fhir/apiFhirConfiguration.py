import sys

api_fhir = sys.modules["api_fhir"]


class ApiFhirConfiguration(object):
    @classmethod
    def getDefaultAuditUserId(cls):
        return api_fhir.default_audit_user_id
