from api_fhir.configurations import ClaimConfiguration


class Stu3ClaimConfig(ClaimConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_claim_config = cfg['stu3_fhir_claim_config']

    @classmethod
    def get_fhir_claim_information_guarantee_id_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_information_guarantee_id_code', "guarantee_id")

    @classmethod
    def get_fhir_claim_item_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_item_code', "item")

    @classmethod
    def get_fhir_claim_service_code(cls):
        return cls.get_config().stu3_fhir_claim_config.get('fhir_claim_service_code', "service")
