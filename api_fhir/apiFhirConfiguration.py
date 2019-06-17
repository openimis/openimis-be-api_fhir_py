import sys

api_fhir = sys.modules["api_fhir"]


class ApiFhirConfiguration(object):
    @classmethod
    def get_default_audit_user_id(cls):
        return api_fhir.default_audit_user_id

    @classmethod
    def get_iso_date_format(cls):
        return api_fhir.iso_date_format

    @classmethod
    def get_iso_datetime_format(cls):
        return api_fhir.iso_datetime_format

    @classmethod
    def get_male_gender_code(cls):
        return api_fhir.gender_codes.get('male', 'M')

    @classmethod
    def get_female_gender_code(cls):
        return api_fhir.gender_codes.get('female', 'F')

    @classmethod
    def get_other_gender_code(cls):
        return api_fhir.gender_codes.get('other', 'O')

    @classmethod
    def get_fhir_identifier_type_system(cls):
        return api_fhir.fhir_identifier_type_config.get('system', "https://hl7.org/fhir/valueset-identifier-type.html")

    @classmethod
    def get_fhir_id_type_code(cls):
        return api_fhir.fhir_identifier_type_config.get('fhir_code_for_imis_db_id_type', "ACSN")

    @classmethod
    def get_fhir_chfid_type_code(cls):
        return api_fhir.fhir_identifier_type_config.get('fhir_code_for_imis_chfid_type', "SB")

    @classmethod
    def get_fhir_passport_type_code(cls):
        return api_fhir.fhir_identifier_type_config.get('fhir_code_for_imis_passport_type', "PPN")

    @classmethod
    def get_fhir_facility_id_type(cls):
        return api_fhir.fhir_identifier_type_config.get('fhir_code_for_imis_facility_id_type', "FI")

    @classmethod
    def get_fhir_location_role_type_system(cls):
        return api_fhir.fhir_location_role_type.get('system',
                                                    "https://hl7.org/fhir/STU3/v3/ServiceDeliveryLocationRoleType/vs.html")

    @classmethod
    def get_fhir_code_for_hospital(cls):
        return api_fhir.fhir_location_role_type.get('fhir_code_for_hospital', "HOSP")

    @classmethod
    def get_fhir_code_for_dispensary(cls):
        return api_fhir.fhir_location_role_type.get('fhir_code_for_dispensary', "CSC")

    @classmethod
    def get_fhir_code_for_health_center(cls):
        return api_fhir.fhir_location_role_type.get('fhir_code_for_health_center', "PC")

    @classmethod
    def get_fhir_marital_status_system(cls):
        return api_fhir.fhir_marital_status_config.get('system',
                                                       "https://www.hl7.org/fhir/STU3/valueset-marital-status.html")

    @classmethod
    def get_fhir_married_code(cls):
        return api_fhir.fhir_marital_status_config.get('fhir_code_for_married', "M")

    @classmethod
    def get_fhir_never_married_code(cls):
        return api_fhir.fhir_marital_status_config.get('fhir_code_for_never_married', "S")

    @classmethod
    def get_fhir_divorced_code(cls):
        return api_fhir.fhir_marital_status_config.get('fhir_code_for_divorced', "D")

    @classmethod
    def get_fhir_widowed_code(cls):
        return api_fhir.fhir_marital_status_config.get('fhir_code_for_widowed', "W")

    @classmethod
    def get_fhir_unknown_marital_status_code(cls):
        return api_fhir.fhir_marital_status_config.get('fhir_code_for_unknown', "U")

    @classmethod
    def get_default_value_of_patient_head_attribute(cls):
        return api_fhir.fhir_marital_status_config.get('default_value_of_patient_head_attribute', False)

    @classmethod
    def get_default_value_of_patient_card_issued_attribute(cls):
        return api_fhir.fhir_marital_status_config.get('default_value_of_patient_card_issued_attribute', False)

    @classmethod
    def get_default_value_of_location_offline_attribute(cls):
        return api_fhir.fhir_marital_status_config.get('default_value_of_location_offline_attribute', False)

    @classmethod
    def get_default_value_of_location_care_type(cls):
        return api_fhir.fhir_marital_status_config.get('default_value_of_location_care_type', "B")
