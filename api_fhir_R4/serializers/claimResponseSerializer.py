from api_fhir_R4.converters import ClaimResponseConverter
from api_fhir_R4.serializers import BaseFHIRSerializer


class ClaimResponseSerializer(BaseFHIRSerializer):

    fhirConverter = ClaimResponseConverter
