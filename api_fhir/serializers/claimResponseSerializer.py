from api_fhir.converters import ClaimResponseConverter
from api_fhir.serializers import BaseFHIRSerializer


class ClaimResponseSerializer(BaseFHIRSerializer):

    fhirConverter = ClaimResponseConverter
