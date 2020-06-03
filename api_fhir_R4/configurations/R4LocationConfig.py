from api_fhir_R4.configurations import LocationConfiguration


class R4LocationConfig(LocationConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().R4_fhir_location_role_type = cfg['R4_fhir_location_role_type']

    @classmethod
    def get_fhir_location_role_type_system(cls):
        return cls.get_config().R4_fhir_location_role_type.get('system',
                                                "http://hl7.org/fhir/v3/ServiceDeliveryLocationRoleType/vs.html")

    @classmethod
    def get_fhir_code_for_hospital(cls):
        return cls.get_config().R4_fhir_location_role_type.get('fhir_code_for_hospital', "HOSP")

    @classmethod
    def get_fhir_code_for_dispensary(cls):
        return cls.get_config().R4_fhir_location_role_type.get('fhir_code_for_dispensary', "CSC")

    @classmethod
    def get_fhir_code_for_health_center(cls):
        return cls.get_config().R4_fhir_location_role_type.get('fhir_code_for_health_center', "PC")
