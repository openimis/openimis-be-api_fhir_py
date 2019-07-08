from api_fhir.configurations import MaritalConfiguration


class Stu3MaritalConfig(MaritalConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_marital_status_config = cfg['stu3_fhir_marital_status_config']

    @classmethod
    def get_fhir_marital_status_system(cls):
        return cls.get_config().stu3_fhir_marital_status_config.get('system',
                                                       "https://www.hl7.org/fhir/STU3/valueset-marital-status.html")

    @classmethod
    def get_fhir_married_code(cls):
        return cls.get_config().stu3_fhir_marital_status_config.get('fhir_code_for_married', "M")

    @classmethod
    def get_fhir_never_married_code(cls):
        return cls.get_config().stu3_fhir_marital_status_config.get('fhir_code_for_never_married', "S")

    @classmethod
    def get_fhir_divorced_code(cls):
        return cls.get_config().stu3_fhir_marital_status_config.get('fhir_code_for_divorced', "D")

    @classmethod
    def get_fhir_widowed_code(cls):
        return cls.get_config().stu3_fhir_marital_status_config.get('fhir_code_for_widowed', "W")

    @classmethod
    def get_fhir_unknown_marital_status_code(cls):
        return cls.get_config().stu3_fhir_marital_status_config.get('fhir_code_for_unknown', "U")
