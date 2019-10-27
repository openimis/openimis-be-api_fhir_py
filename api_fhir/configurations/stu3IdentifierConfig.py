from api_fhir.configurations import IdentifierConfiguration


class Stu3IdentifierConfig(IdentifierConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_identifier_type_config = cfg['stu3_fhir_identifier_type_config']

    @classmethod
    def get_fhir_identifier_type_system(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('system',
                                                                "https://hl7.org/fhir/valueset-identifier-type.html")

    @classmethod
    def get_fhir_uuid_type_code(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_imis_db_id_type', "ACSN")

    @classmethod
    def get_fhir_chfid_type_code(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_imis_chfid_type', "SB")

    @classmethod
    def get_fhir_passport_type_code(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_imis_passport_type', "PPN")

    @classmethod
    def get_fhir_facility_id_type(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_imis_facility_id_type', "FI")

    @classmethod
    def get_fhir_claim_admin_code_type(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_imis_claim_admin_code_type', "FILL")

    @classmethod
    def get_fhir_claim_code_type(cls):
        return cls.get_config().stu3_fhir_identifier_type_config.get('fhir_code_for_imis_claim_code_type', "MR")
