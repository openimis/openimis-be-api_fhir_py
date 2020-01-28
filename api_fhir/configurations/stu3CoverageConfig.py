from api_fhir.configurations import CoverageConfiguration


class Stu3CoverageConfig(CoverageConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_identifier_type_config = cfg['stu3_fhir_coverage_config']

    @classmethod
    def get_family_reference_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_family_refereence_code', "FamilyReference")

    @classmethod
    def get_status_idle_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_status_idle_code', "Idle")

    @classmethod
    def get_status_active_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_status_active_code', "active")

    @classmethod
    def get_status_suspended_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_status_suspended_code', "suspended")

    @classmethod
    def get_status_expired_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_status_expired_code', "Expired")

    @classmethod
    def get_item_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_item_code', "item")

    @classmethod
    def get_service_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_service_code', "service")

    @classmethod
    def get_practitioner_role_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_practitioner_role_code', "Practitioner")

    @classmethod
    def get_product_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_product_code', "Product")

    @classmethod
    def get_enroll_date_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_enroll_date_code', "EnrollDate")

    @classmethod
    def get_effective_date_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_effective_date_code', "EffectiveDate")
