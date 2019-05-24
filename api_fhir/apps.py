import logging
import sys

from django.apps import AppConfig

logger = logging.getLogger(__name__)

MODULE_NAME = "api_fhir"

this = sys.modules[MODULE_NAME]

DEFAULT_CFG = {
    "default_audit_user_id": 1,
    "iso_date_format": "%Y-%m-%d",
    "iso_datetime_format": "%Y-%m-%dT%H:%M:%S",
    "gender_codes": {
        "male": "M",
        "female": "F",
        "other": "O"
    },
    "fhir_identifier_type_config": {
        "system": "https://hl7.org/fhir/valueset-identifier-type.html",
        "fhir_code_for_imis_db_id_type": "ACSN",
        "fhir_code_for_imis_chfid_type": "SB",
        "fhir_code_for_imis_passport_type": "PPN"
    },
    "fhir_marital_status_config": {
        "system": "https://www.hl7.org/fhir/STU3/valueset-marital-status.html",
        "fhir_code_for_married": "M",
        "fhir_code_for_never_married": "S",
        "fhir_code_for_divorced": "D",
        "fhir_code_for_widowed": "W",
        "fhir_code_for_unknown": "U"
    }
}

class ApiFhirConfig(AppConfig):
    name = MODULE_NAME

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__configure_module(cfg)

    def __configure_module(self, cfg):
        this.default_audit_user_id = cfg['default_audit_user_id']
        this.gender_codes = cfg['gender_codes']
        this.iso_date_format = cfg['iso_date_format']
        this.iso_datetime_format = cfg['iso_datetime_format']
        this.fhir_identifier_type_config = cfg['fhir_identifier_type_config']
        this.fhir_marital_status_config = cfg['fhir_marital_status_config']
        logger.info('Module $s configured successfully', MODULE_NAME)
