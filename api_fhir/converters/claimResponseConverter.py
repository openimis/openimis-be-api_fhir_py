from api_fhir.configurations import Stu3ClaimConfig
from api_fhir.converters import BaseFHIRConverter
from api_fhir.models import ClaimResponse
from api_fhir.utils import TimeUtils


class ClaimResponseConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim):
        claim_response = ClaimResponse()
        cls.build_fhir_pk(claim_response, imis_claim.code)
        claim_response.created = TimeUtils.now().isoformat()
        cls.build_fhir_outcome(claim_response, imis_claim)
        return claim_response

    @classmethod
    def build_fhir_outcome(cls, claim_response, imis_claim):
        code = imis_claim.status
        if code is not None:
            status_display = None
            if code == 1:
                status_display = Stu3ClaimConfig.get_fhir_claim_status_rejected_code()
            elif code == 2:
                status_display = Stu3ClaimConfig.get_fhir_claim_status_entered_code()
            elif code == 4:
                status_display = Stu3ClaimConfig.get_fhir_claim_status_checked_code()
            elif code == 8:
                status_display = Stu3ClaimConfig.get_fhir_claim_status_processed_code()
            elif code == 16:
                status_display = Stu3ClaimConfig.get_fhir_claim_status_valuated_code()
            claim_response.outcome = cls.build_codeable_concept(imis_claim.status, system=None, text=status_display)
