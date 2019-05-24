import logging
import sys

from django.apps import AppConfig

logger = logging.getLogger(__name__)

MODULE_NAME = "api_fhir"

this = sys.modules[MODULE_NAME]

DEFAULT_CFG = {
    "default_audit_user_id": 1,
    "gender_codes": {
        "male": "M",
        "female": "F",
        "other": "O"
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
        logger.info('Module $s configured successfully', MODULE_NAME)
