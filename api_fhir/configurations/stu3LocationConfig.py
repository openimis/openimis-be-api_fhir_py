from api_fhir.configurations import LocationConfiguration


class Stu3LocationConfig(LocationConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_location_role_type = cfg['stu3_fhir_location_role_type']

    @classmethod
    def get_fhir_location_role_type_system(cls):
        return cls.get_config().stu3_fhir_location_role_type.get('system',
                                                "https://hl7.org/fhir/STU3/v3/ServiceDeliveryLocationRoleType/vs.html")

    @classmethod
    def get_fhir_code_for_hospital(cls):
        return cls.get_config().stu3_fhir_location_role_type.get('fhir_code_for_hospital', "HOSP")

    @classmethod
    def get_fhir_code_for_dispensary(cls):
        return cls.get_config().stu3_fhir_location_role_type.get('fhir_code_for_dispensary', "CSC")

    @classmethod
    def get_fhir_code_for_health_center(cls):
        return cls.get_config().stu3_fhir_location_role_type.get('fhir_code_for_health_center', "PC")
