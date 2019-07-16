from api_fhir.converters import CommunicationRequestConverter
from api_fhir.serializers import BaseFHIRSerializer


class CommunicationRequestSerializer(BaseFHIRSerializer):

    fhirConverter = CommunicationRequestConverter
