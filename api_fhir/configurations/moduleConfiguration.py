from api_fhir.configurations import BaseConfiguration, GeneralConfiguration, Stu3ApiFhirConfig
from django.conf import settings


class ModuleConfiguration(BaseConfiguration):

    __REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'api_fhir.exceptions.fhir_api_exception_handler'
    }

    @classmethod
    def build_configuration(cls, cfg):
        GeneralConfiguration.build_configuration(cfg)
        cls.get_stu3().build_configuration(cfg)
        cls.configure_api_error_handler()

    @classmethod
    def get_stu3(cls):
        return Stu3ApiFhirConfig

    @classmethod
    def configure_api_error_handler(cls):
        config = cls.get_config()
        rest_settings = settings.__getattr__("REST_FRAMEWORK")
        config.default_api_error_handler = rest_settings.get("EXCEPTION_HANDLER")
        rest_settings.update(cls.__REST_FRAMEWORK)

    @classmethod
    def get_default_api_error_handler(cls):
        return cls.get_config().default_api_error_handler
