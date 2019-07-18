from api_fhir.configurations import ClaimConfiguration


class Stu3ClaimConfig(ClaimConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_claim_config = cfg['stu3_fhir_claim_config']

    @classmethod
    def get_fhir_claim_information_guarantee_id_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_information_guarantee_id_code', "guarantee_id")

    @classmethod
    def get_fhir_claim_information_explanation_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_information_explanation_code', "explanation")

    @classmethod
    def get_fhir_claim_item_explanation_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_explanation_code', "item_explanation")

    @classmethod
    def get_fhir_claim_item_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_code', "item")

    @classmethod
    def get_fhir_claim_service_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_service_code', "service")

    @classmethod
    def get_fhir_claim_status_rejected_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_status_rejected_code', "rejected")

    @classmethod
    def get_fhir_claim_status_entered_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_status_entered_code', "entered")

    @classmethod
    def get_fhir_claim_status_checked_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_status_checked_code', "checked")

    @classmethod
    def get_fhir_claim_status_processed_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_status_processed_code', "processed")

    @classmethod
    def get_fhir_claim_status_valuated_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_status_valuated_code', "valuated")

    @classmethod
    def get_fhir_claim_item_status_passed_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_status_passed_code', "passed")

    @classmethod
    def get_fhir_claim_item_status_rejected_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_status_rejected_code', "rejected")

    @classmethod
    def get_fhir_claim_item_general_adjudication_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_general_adjudication_code', "general")

    @classmethod
    def get_fhir_claim_item_rejected_reason_adjudication_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_rejected_reason_adjudication_code',
                                                           "rejected_reason")
