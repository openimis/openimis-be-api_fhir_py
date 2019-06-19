from api_fhir.configurations import BaseConfiguration


class GeneralConfiguration(BaseConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        config = cls.get_config()
        config.default_audit_user_id = cfg['default_audit_user_id']
        config.iso_date_format = cfg['iso_date_format']
        config.iso_datetime_format = cfg['iso_datetime_format']
        config.gender_codes = cfg['gender_codes']
        config.default_value_of_patient_head_attribute = cfg['default_value_of_patient_head_attribute']
        config.default_value_of_patient_card_issued_attribute = cfg['default_value_of_patient_card_issued_attribute']
        config.default_value_of_location_offline_attribute = cfg['default_value_of_location_offline_attribute']
        config.default_value_of_location_care_type = cfg['default_value_of_location_care_type']

    @classmethod
    def get_default_audit_user_id(cls):
        return cls.get_config().default_audit_user_id

    @classmethod
    def get_iso_date_format(cls):
        return cls.get_config().iso_date_format

    @classmethod
    def get_iso_datetime_format(cls):
        return cls.get_config().iso_datetime_format

    @classmethod
    def get_male_gender_code(cls):
        return cls.get_config().gender_codes.get('male', 'M')

    @classmethod
    def get_female_gender_code(cls):
        return cls.get_config().gender_codes.get('female', 'F')

    @classmethod
    def get_other_gender_code(cls):
        return cls.get_config().gender_codes.get('other', 'O')

    @classmethod
    def get_default_value_of_patient_head_attribute(cls):
        return cls.get_config().default_value_of_patient_head_attribute

    @classmethod
    def get_default_value_of_patient_card_issued_attribute(cls):
        return cls.get_config().default_value_of_patient_card_issued_attribute

    @classmethod
    def get_default_value_of_location_offline_attribute(cls):
        return cls.get_config().default_value_of_location_offline_attribute

    @classmethod
    def get_default_value_of_location_care_type(cls):
        return cls.get_config().default_value_of_location_care_type

    class Meta:
        app_label = 'api_fhir'