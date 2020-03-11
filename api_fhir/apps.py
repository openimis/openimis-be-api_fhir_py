import logging

from django.apps import AppConfig

from api_fhir.configurations import ModuleConfiguration

logger = logging.getLogger(__name__)

MODULE_NAME = "api_fhir"

DEFAULT_CFG = {
    "default_audit_user_id": 1,
    "gender_codes": {
        "male": "M",
        "female": "F",
        "other": "O"
    },
    "default_value_of_patient_head_attribute": False,
    "default_value_of_patient_card_issued_attribute": False,
    "default_value_of_location_offline_attribute": False,
    "default_value_of_location_care_type": "B",
    "default_response_page_size": 10,
    "stu3_fhir_identifier_type_config": {
        "system": "https://hl7.org/fhir/valueset-identifier-type.html",
        "fhir_code_for_imis_db_id_type": "ACSN",
        "fhir_code_for_imis_chfid_type": "SB",
        "fhir_code_for_imis_passport_type": "PPN",
        "fhir_code_for_imis_facility_id_type": "FI",
        "fhir_code_for_imis_claim_admin_code_type": "FILL",
        "fhir_code_for_imis_claim_code_type": "MR",
    },
    "stu3_fhir_marital_status_config": {
        "system": "https://www.hl7.org/fhir/STU3/valueset-marital-status.html",
        "fhir_code_for_married": "M",
        "fhir_code_for_never_married": "S",
        "fhir_code_for_divorced": "D",
        "fhir_code_for_widowed": "W",
        "fhir_code_for_unknown": "U"
    },
    "stu3_fhir_location_role_type": {
        "system": "https://www.hl7.org/fhir/STU3/v3/ServiceDeliveryLocationRoleType/vs.html",
        "fhir_code_for_hospital": "HOSP",
        "fhir_code_for_dispensary": "CSC",
        "fhir_code_for_health_center": "PC",
    },
    "stu3_fhir_issue_type_config": {
        "fhir_code_for_exception": "exception",
        "fhir_code_for_not_found": "not-found",
        "fhir_code_for_informational": "informational"
    },
    "stu3_fhir_claim_config": {
        "fhir_claim_information_guarantee_id_code": "guarantee_id",
        "fhir_claim_information_explanation_code": "explanation",
        "fhir_claim_item_explanation_code": "item_explanation",
        "fhir_claim_item_code": "item",
        "fhir_claim_service_code": "service",
        "fhir_claim_status_rejected_code": "rejected",
        "fhir_claim_status_entered_code": "entered",
        "fhir_claim_status_checked_code": "checked",
        "fhir_claim_status_processed_code": "processed",
        "fhir_claim_status_valuated_code": "valuated",
        "fhir_claim_item_status_code": "claim_item_status",
        "fhir_claim_item_status_passed_code": "passed",
        "fhir_claim_item_status_rejected_code": "rejected",
        "fhir_claim_item_general_adjudication_code": "general",
        "fhir_claim_item_rejected_reason_adjudication_code": "rejected_reason",
    },
    "stu3_fhir_eligibility_config": {
        "fhir_serializer": "PolicyEligibilityRequestSerializer",
        "fhir_item_code": "item",
        "fhir_service_code": "service",
        "fhir_total_admissions_code": "total_admissions",
        "fhir_total_visits_code": "total_visits",
        "fhir_total_consultations_code": "total_consultations",
        "fhir_total_surgeries_code": "total_surgeries",
        "fhir_total_deliveries_code": "total_deliveries",
        "fhir_total_antenatal_code": "total_antenatal",
        "fhir_consultation_amount_code": "consultation_amount",
        "fhir_surgery_amount_code": "surgery_amount",
        "fhir_delivery_amount_code": "delivery_amount",
        "fhir_hospitalization_amount_code": "hospitalization_amount",
        "fhir_antenatal_amount_code": "antenatal_amount",
        "fhir_service_left_code": "service_left",
        "fhir_item_left_code": "item_left",
        "fhir_is_item_ok_code": "is_item_ok",
        "fhir_is_service_ok_code": "is_service_ok",
        "fhir_balance_code": "balance",
        "fhir_balance_default_category": "medical",
        "fhir_active_policy_status": ("A", 2)
    },
    "stu3_fhir_communication_request_config": {
        "fhir_care_rendered_code": "care_rendered",
        "fhir_payment_asked_code": "payment_asked",
        "fhir_drug_prescribed_code": "drug_prescribed",
        "fhir_drug_received_code": "drug_received",
        "fhir_asessment_code": "asessment"
    },
    "stu3_fhir_coverage_config": {
        "fhir_family_refereence_code": "FamilyReference",
        "fhir_status_idle_code": "Idle",
        "fhir_status_active_code": "active",
        "fhir_status_suspended_code": "suspended",
        "fhir_status_expired_code": "Expired",
        "fhir_item_code": "item",
        "fhir_service_code": "service",
        "fhir_practitioner_role_code": "Practitioner",
        "fhir_product_code": "Product",
        "fhir_effective_date_code": "EffectiveDate",
        "fhir_enroll_date_code": "EnrollDate"
    }
}


class ApiFhirConfig(AppConfig):
    name = MODULE_NAME

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__configure_module(cfg)

    def __configure_module(self, cfg):
        ModuleConfiguration.build_configuration(cfg)
        logger.info('Module $s configured successfully', MODULE_NAME)
