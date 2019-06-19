from api_fhir.configurations import BaseConfiguration, GeneralConfiguration, Stu3ApiFhirConfig


class ModuleConfiguration(BaseConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        GeneralConfiguration.build_configuration(cfg)
        cls.get_stu3().build_configuration(cfg)

    @classmethod
    def get_stu3(cls):
        return Stu3ApiFhirConfig

    class Meta:
        app_label = 'api_fhir'