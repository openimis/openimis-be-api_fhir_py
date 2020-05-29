import logging

from policy.services import ByInsureeRequest, ByInsureeService, ByInsureeResponse

from api_fhir.converters import PolicyEligibilityRequestConverter
from api_fhir.serializers import BaseFHIRSerializer


class PolicyEligibilityRequestSerializer(BaseFHIRSerializer):

    fhirConverter = PolicyEligibilityRequestConverter()
    logger = logging.getLogger(__name__)

    def create(self, validated_data):
        eligibility_request = ByInsureeRequest(chf_id=validated_data.get('chf_id'))
        request = self.context.get("request")
        try:
            response = ByInsureeService(request.user).request(eligibility_request)            
        except TypeError:
            self.logger.warning('The insuree with chfid `{}` is not connected with policy. '
                                'The default eligibility response will be used.'
                                .format(validated_data.get('chfid')))
            response = self.create_default_eligibility_response()
        return response

    def create_default_eligibility_response(self):
        return ByInsureeResponse(
            eligibility_request=None,
            items=[]
        )
