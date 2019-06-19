from api_fhir.configurations import BaseApiFhirConfiguration, Stu3IdentifierConfig, \
    Stu3LocationConfig, Stu3MaritalConfig


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

    class Meta:
        app_label = 'api_fhir'
