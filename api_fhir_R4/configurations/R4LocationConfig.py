from api_fhir_R4.configurations import LocationConfiguration


class R4LocationConfig(LocationConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().R4_fhir_location_role_type = cfg['R4_fhir_location_role_type']
        cls.get_config().R4_fhir_location_physical_type = cfg['R4_fhir_location_physical_type']

    @classmethod
    def get_fhir_location_role_type_system(cls):
        return cls.get_config().R4_fhir_location_role_type.get('system',
                                                "http://hl7.org/fhir/v3/ServiceDeliveryLocationRoleType/vs.html")

    @classmethod
    def get_fhir_code_for_hospital(cls):
        return cls.get_config().R4_fhir_location_role_type.get('fhir_code_for_hospital', "H")

    @classmethod
    def get_fhir_code_for_dispensary(cls):
        return cls.get_config().R4_fhir_location_role_type.get('fhir_code_for_dispensary', "D")

    @classmethod
    def get_fhir_code_for_health_center(cls):
        return cls.get_config().R4_fhir_location_role_type.get('fhir_code_for_health_center', "C")

    @classmethod
    def get_fhir_location_physical_type_system(cls):
        return cls.get_config().R4_fhir_location_physical_type.get('system',
                                                "http://terminology.hl7.org/CodeSystem/location-physical-type.html")

    @classmethod
    def get_fhir_code_for_region(cls):
        return cls.get_config().R4_fhir_location_physical_type.get('fhir_code_for_region', "R")

    @classmethod
    def get_fhir_code_for_district(cls):
        return cls.get_config().R4_fhir_location_physical_type.get('fhir_code_for_district', "D")

    @classmethod
    def get_fhir_code_for_ward(cls):
        return cls.get_config().R4_fhir_location_physical_type.get('fhir_code_for_ward', "W")

    @classmethod
    def get_fhir_code_for_village(cls):
        return cls.get_config().R4_fhir_location_physical_type.get('fhir_code_for_village', "V")
