import logging

from django.apps import AppConfig

from api_fhir.configurations import ModuleConfiguration

logger = logging.getLogger(__name__)

MODULE_NAME = "api_fhir"

DEFAULT_CFG = {
    "default_audit_user_id": 1,
    "iso_date_format": "%Y-%m-%d",
    "iso_datetime_format": "%Y-%m-%dT%H:%M:%S",
    "gender_codes": {
        "male": "M",
        "female": "F",
        "other": "O"
    },
    "default_value_of_patient_head_attribute": False,
    "default_value_of_patient_card_issued_attribute": False,
    "default_value_of_location_offline_attribute": False,
    "default_value_of_location_care_type": "B",
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
        "fhir_claim_item_code": "item",
        "fhir_claim_service_code": "service"
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
