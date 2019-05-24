import sys

api_fhir = sys.modules["api_fhir"]


class ApiFhirConfiguration(object):
    @classmethod
    def get_default_audit_user_id(cls):
        return api_fhir.default_audit_user_id

    @classmethod
    def get_male_gender_code(cls):
        return api_fhir.gender_codes.get('male', 'M')

    @classmethod
    def get_female_gender_code(cls):
        return api_fhir.gender_codes.get('female', 'F')

    @classmethod
    def get_other_gender_code(cls):
        return api_fhir.gender_codes.get('other', 'O')
