from api_fhir.configurations import BaseApiFhirConfiguration, Stu3IdentifierConfig, \
    Stu3LocationConfig, Stu3MaritalConfig, Stu3IssueTypeConfig, Stu3ClaimConfig, Stu3EligibilityConfiguration, \
    Stu3CommunicationRequestConfig
from api_fhir.configurations.stu3CoverageConfig import Stu3CoverageConfig


class Stu3ApiFhirConfig(BaseApiFhirConfiguration):

    @classmethod
    def get_identifier_configuration(cls):
        return Stu3IdentifierConfig

    @classmethod
    def get_location_type_configuration(cls):
        return Stu3LocationConfig

    @classmethod
    def get_marital_type_configuration(cls):
        return Stu3MaritalConfig

    @classmethod
    def get_issue_type_configuration(cls):
        return Stu3IssueTypeConfig

    @classmethod
    def get_claim_configuration(cls):
        return Stu3ClaimConfig

    @classmethod
    def get_eligibility_configuration(cls):
        return Stu3EligibilityConfiguration

    @classmethod
    def get_communication_request_configuration(cls):
        return Stu3CommunicationRequestConfig

    @classmethod
    def get_coverage_configuration(cls):
        return Stu3CoverageConfig
