from api_fhir_R4.configurations import BaseConfiguration, GeneralConfiguration, R4ApiFhirConfig
from django.conf import settings


class ModuleConfiguration(BaseConfiguration):

    __REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'api_fhir_R4.exceptions.fhir_api_exception_handler'
    }

    @classmethod
    def build_configuration(cls, cfg):
        GeneralConfiguration.build_configuration(cfg)
        cls.get_R4().build_configuration(cfg)
        cls.configure_api_error_handler()

    @classmethod
    def get_R4(cls):
        return R4ApiFhirConfig

    @classmethod
    def configure_api_error_handler(cls):
        config = cls.get_config()
        rest_settings = settings.__getattr__("REST_FRAMEWORK")
        config.default_api_error_handler = rest_settings.get("EXCEPTION_HANDLER")
        rest_settings.update(cls.__REST_FRAMEWORK)

    @classmethod
    def get_default_api_error_handler(cls):
        return cls.get_config().default_api_error_handler
