import sys


class BaseConfiguration(object):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_config(cls):
        module_name = "api_fhir"
        return sys.modules[module_name]


class IdentifierConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_identifier_type_system(cls):
        raise NotImplementedError('`get_fhir_identifier_type_system()` must be implemented.')

    @classmethod
    def get_fhir_uuid_type_code(cls):
        raise NotImplementedError('`get_fhir_id_type_code()` must be implemented.')

    @classmethod
    def get_fhir_chfid_type_code(cls):
        raise NotImplementedError('`get_fhir_chfid_type_code()` must be implemented.')

    @classmethod
    def get_fhir_passport_type_code(cls):
        raise NotImplementedError('`get_fhir_passport_type_code()` must be implemented.')

    @classmethod
    def get_fhir_facility_id_type(cls):
        raise NotImplementedError('`get_fhir_facility_id_type()` must be implemented.')

    @classmethod
    def get_fhir_claim_admin_code_type(cls):
        raise NotImplementedError('`get_fhir_claim_admin_code_type()` must be implemented.')

    @classmethod
    def get_fhir_claim_code_type(cls):
        raise NotImplementedError('`get_fhir_claim_code_type()` must be implemented.')


class LocationConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_location_role_type_system(cls):
        raise NotImplementedError('`get_fhir_location_role_type_system()` must be implemented.')

    @classmethod
    def get_fhir_code_for_hospital(cls):
        raise NotImplementedError('`get_fhir_code_for_hospital()` must be implemented.')

    @classmethod
    def get_fhir_code_for_dispensary(cls):
        raise NotImplementedError('`get_fhir_code_for_dispensary()` must be implemented.')

    @classmethod
    def get_fhir_code_for_health_center(cls):
        raise NotImplementedError('`get_fhir_code_for_health_center()` must be implemented.')


class MaritalConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_marital_status_system(cls):
        raise NotImplementedError('`get_fhir_marital_status_system()` must be implemented.')

    @classmethod
    def get_fhir_married_code(cls):
        raise NotImplementedError('`get_fhir_married_code()` must be implemented.')

    @classmethod
    def get_fhir_never_married_code(cls):
        raise NotImplementedError('`get_fhir_never_married_code()` must be implemented.')

    @classmethod
    def get_fhir_divorced_code(cls):
        raise NotImplementedError('`get_fhir_divorced_code()` must be implemented.')

    @classmethod
    def get_fhir_widowed_code(cls):
        raise NotImplementedError('`get_fhir_widowed_code()` must be implemented.')

    @classmethod
    def get_fhir_unknown_marital_status_code(cls):
        raise NotImplementedError('`get_fhir_unknown_marital_status_code()` must be implemented.')


class IssueTypeConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_code_for_exception(cls):
        raise NotImplementedError('`get_fhir_code_for_exception()` must be implemented.')

    @classmethod
    def get_fhir_code_for_not_found(cls):
        raise NotImplementedError('`get_fhir_code_for_not_found()` must be implemented.')

    @classmethod
    def get_fhir_code_for_informational(cls):
        raise NotImplementedError('`get_fhir_code_for_informational()` must be implemented.')

    @classmethod
    def get_fhir_claim_item_general_adjudication_code(cls):
        raise NotImplementedError('`get_fhir_claim_item_general_adjudication_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_item_rejected_reason_adjudication_code(cls):
        raise NotImplementedError('`get_fhir_claim_item_rejected_reason_adjudication_code()` must be implemented.')


class ClaimConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_claim_information_guarantee_id_code(cls):
        raise NotImplementedError('`get_fhir_claim_information_guarantee_id_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_information_explanation_code(cls):
        raise NotImplementedError('`get_fhir_claim_information_explanation_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_item_explanation_code(cls):
        raise NotImplementedError('`get_fhir_claim_item_explanation_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_item_code(cls):
        raise NotImplementedError('`get_fhir_claim_item_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_service_code(cls):
        raise NotImplementedError('`get_fhir_claim_service_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_status_rejected_code(cls):
        raise NotImplementedError('`get_fhir_claim_status_rejected_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_status_entered_code(cls):
        raise NotImplementedError('`get_fhir_claim_status_entered_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_status_checked_code(cls):
        raise NotImplementedError('`get_fhir_claim_status_checked_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_status_processed_code(cls):
        raise NotImplementedError('`get_fhir_claim_status_processed_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_status_valuated_code(cls):
        raise NotImplementedError('`get_fhir_claim_status_valuated_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_item_status_passed_code(cls):
        raise NotImplementedError('`get_fhir_claim_item_status_passed_code()` must be implemented.')

    @classmethod
    def get_fhir_claim_item_status_rejected_code(cls):
        raise NotImplementedError('`get_fhir_claim_item_status_rejected_code()` must be implemented.')


class EligibilityConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_financial_code(cls):
        raise NotImplementedError('`get_fhir_financial_code()` must be implemented.')

    @classmethod
    def get_fhir_item_code(cls):
        raise NotImplementedError('`get_fhir_item_code()` must be implemented.')

    @classmethod
    def get_fhir_service_code(cls):
        raise NotImplementedError('`get_fhir_service_code()` must be implemented.')

    @classmethod
    def get_fhir_total_admissions_code(cls):
        raise NotImplementedError('`get_fhir_total_admissions_code()` must be implemented.')

    @classmethod
    def get_fhir_total_visits_code(cls):
        raise NotImplementedError('`get_fhir_total_visits_code()` must be implemented.')

    @classmethod
    def get_fhir_total_consultations_code(cls):
        raise NotImplementedError('`get_fhir_total_consultations_code()` must be implemented.')

    @classmethod
    def get_fhir_total_surgeries_code(cls):
        raise NotImplementedError('`get_fhir_total_surgeries_code()` must be implemented.')

    @classmethod
    def get_fhir_total_deliveries_code(cls):
        raise NotImplementedError('`get_fhir_total_deliveries_code()` must be implemented.')

    @classmethod
    def get_fhir_total_antenatal_code(cls):
        raise NotImplementedError('`get_fhir_total_antenatal_code()` must be implemented.')

    @classmethod
    def get_fhir_consultation_amount_code(cls):
        raise NotImplementedError('`get_fhir_consultation_amount_code()` must be implemented.')

    @classmethod
    def get_fhir_surgery_amount_code(cls):
        raise NotImplementedError('`get_fhir_surgery_amount_code()` must be implemented.')

    @classmethod
    def get_fhir_delivery_amount_code(cls):
        raise NotImplementedError('`get_fhir_delivery_amount_code()` must be implemented.')

    @classmethod
    def get_fhir_hospitalization_amount_code(cls):
        raise NotImplementedError('`get_fhir_hospitalization_amount_code()` must be implemented.')

    @classmethod
    def get_fhir_antenatal_amount_code(cls):
        raise NotImplementedError('`get_fhir_antenatal_amount_code()` must be implemented.')

    @classmethod
    def get_fhir_service_left_code(cls):
        raise NotImplementedError('`get_fhir_service_left_code()` must be implemented.')

    @classmethod
    def get_fhir_item_left_code(cls):
        raise NotImplementedError('`get_fhir_item_left_code()` must be implemented.')

    @classmethod
    def get_fhir_is_item_ok_code(cls):
        raise NotImplementedError('`get_fhir_is_item_ok_code()` must be implemented.')

    @classmethod
    def get_fhir_is_service_ok_code(cls):
        raise NotImplementedError('`get_fhir_is_service_ok_code()` must be implemented.')

    @classmethod
    def get_fhir_balance_code(cls):
        raise NotImplementedError('`get_fhir_balance_code()` must be implemented.')

    @classmethod
    def get_fhir_balance_default_category(cls):
        raise NotImplementedError('`get_fhir_balance_default_category()` must be implemented.')

    @classmethod
    def get_fhir_status_map(cls):
        raise NotImplementedError('`get_fhir_status_map()` must be implemented.')        
 

class CommunicationRequestConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_fhir_care_rendered_code(cls):
        raise NotImplementedError('`get_fhir_care_rendered_code()` must be implemented.')

    @classmethod
    def get_fhir_payment_asked_code(cls):
        raise NotImplementedError('`get_fhir_payment_asked_code()` must be implemented.')

    @classmethod
    def get_fhir_drug_prescribed_code(cls):
        raise NotImplementedError('`get_fhir_drug_prescribed_code()` must be implemented.')

    @classmethod
    def get_fhir_drug_received_code(cls):
        raise NotImplementedError('`get_fhir_care_rendered_code()` must be implemented.')

    @classmethod
    def get_fhir_asessment_code(cls):
        raise NotImplementedError('`get_fhir_asessment_code()` must be implemented.')


class CoverageConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        raise NotImplementedError('`build_configuration()` must be implemented.')

    @classmethod
    def get_family_reference_code(cls):
        raise NotImplementedError('`get_family_reference_code()` must be implemented.')

    @classmethod
    def get_status_idle_code(cls):
        raise NotImplementedError('`get_status_idle_code()` must be implemented.')

    @classmethod
    def get_status_active_code(cls):
        raise NotImplementedError('`get_status_active_code()` must be implemented.')

    @classmethod
    def get_status_suspended_code(cls):
        raise NotImplementedError('`get_status_suspended_code()` must be implemented.')

    @classmethod
    def get_status_expired_code(cls):
        raise NotImplementedError('`get_status_expired_code()` must be implemented.')

    @classmethod
    def get_item_code(cls):
        raise NotImplementedError('`get_item_code()` must be implemented.')

    @classmethod
    def get_service_code(cls):
        raise NotImplementedError('`get_service_code()` must be implemented.')

    @classmethod
    def get_service_code(cls):
        raise NotImplementedError('`get_practitioner_role_code()` must be implemented.')

    @classmethod
    def get_product_code(cls):
        raise NotImplementedError('`get_product_code()` must be implemented.')

    @classmethod
    def get_enroll_date_code(cls):
        raise NotImplementedError('`get_enroll_date_code()` must be implemented.')

    @classmethod
    def get_effective_date_code(cls):
        raise NotImplementedError('`get_effective_date_code()` must be implemented.')


class BaseApiFhirConfiguration(BaseConfiguration):  # pragma: no cover

    @classmethod
    def build_configuration(cls, cfg):
        cls.get_identifier_configuration().build_configuration(cfg)
        cls.get_location_type_configuration().build_configuration(cfg)
        cls.get_marital_type_configuration().build_configuration(cfg)
        cls.get_issue_type_configuration().build_configuration(cfg)
        cls.get_claim_configuration().build_configuration(cfg)
        cls.get_eligibility_configuration().build_configuration(cfg)
        cls.get_communication_request_configuration().build_configuration(cfg)
        cls.get_coverage_configuration().build_configuration(cfg)

    @classmethod
    def get_identifier_configuration(cls):
        raise NotImplementedError('`get_identifier_configuration()` must be implemented.')

    @classmethod
    def get_location_type_configuration(cls):
        raise NotImplementedError('`get_location_type_configuration()` must be implemented.')

    @classmethod
    def get_marital_type_configuration(cls):
        raise NotImplementedError('`get_marital_type_configuration()` must be implemented.')

    @classmethod
    def get_issue_type_configuration(cls):
        raise NotImplementedError('`get_issue_type_configuration()` must be implemented.')

    @classmethod
    def get_claim_configuration(cls):
        raise NotImplementedError('`get_claim_configuration()` must be implemented.')

    @classmethod
    def get_eligibility_configuration(cls):
        raise NotImplementedError('`get_eligibility_configuration()` must be implemented.')

    @classmethod
    def get_communication_request_configuration(cls):
        raise NotImplementedError('`get_communication_request_configuration()` must be implemented.')

    @classmethod
    def get_coverage_configuration(cls):
        raise NotImplementedError('`get_coverage_configuration()` must be implemented.')


from api_fhir.configurations.generalConfiguration import GeneralConfiguration
from api_fhir.configurations.stu3IdentifierConfig import Stu3IdentifierConfig
from api_fhir.configurations.stu3LocationConfig import Stu3LocationConfig
from api_fhir.configurations.stu3MaritalConfig import Stu3MaritalConfig
from api_fhir.configurations.stu3IssueTypeConfig import Stu3IssueTypeConfig
from api_fhir.configurations.stu3ClaimConfig import Stu3ClaimConfig
from api_fhir.configurations.stu3EligibilityConfiguration import Stu3EligibilityConfiguration
from api_fhir.configurations.stu3CommunicationRequestConfig import Stu3CommunicationRequestConfig
from api_fhir.configurations.stu3ApiFhirConfig import Stu3ApiFhirConfig
from api_fhir.configurations.moduleConfiguration import ModuleConfiguration
from api_fhir.configurations.stu3CoverageConfig import Stu3CoverageConfig
