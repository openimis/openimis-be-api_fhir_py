from api_fhir.configurations import CommunicationRequestConfiguration


class Stu3CommunicationRequestConfig(CommunicationRequestConfiguration):

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_config().stu3_fhir_communication_config = cfg['stu3_fhir_communication_request_config']

    @classmethod
    def get_fhir_care_rendered_code(cls):
        return cls.get_config().stu3_fhir_communication_config.get('fhir_care_rendered_code', "care_rendered")

    @classmethod
    def get_fhir_payment_asked_code(cls):
        return cls.get_config().stu3_fhir_communication_config.get('fhir_payment_asked_code', "payment_asked")

    @classmethod
    def get_fhir_drug_prescribed_code(cls):
        return cls.get_config().stu3_fhir_communication_config.get('fhir_drug_prescribed_code', "drug_prescribed")

    @classmethod
    def get_fhir_drug_received_code(cls):
        return cls.get_config().stu3_fhir_communication_config.get('fhir_drug_received_code', "drug_received")

    @classmethod
    def get_fhir_asessment_code(cls):
        return cls.get_config().stu3_fhir_communication_config.get('fhir_asessment_code', "asessment")
