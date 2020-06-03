from api_fhir_R4.converters import CommunicationRequestConverter
from api_fhir_R4.serializers import BaseFHIRSerializer


class CommunicationRequestSerializer(BaseFHIRSerializer):

    fhirConverter = CommunicationRequestConverter
