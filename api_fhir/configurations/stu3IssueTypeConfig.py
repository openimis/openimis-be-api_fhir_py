from api_fhir.configurations import IssueTypeConfiguration


class Stu3IssueTypeConfig(IssueTypeConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_issue_type_config = cfg['stu3_fhir_issue_type_config']

    @classmethod
    def get_fhir_code_for_exception(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_exception', 'exception')

    @classmethod
    def get_fhir_code_for_not_found(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_not_found', 'not-found')

    @classmethod
    def get_fhir_code_for_informational(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_informational', 'informational')
