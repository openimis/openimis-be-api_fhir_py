from api_fhir_R4.converters.coverageConventer import CoverageConventer
from api_fhir_R4.serializers import BaseFHIRSerializer


class CoverageSerializer(BaseFHIRSerializer):

    fhirConverter = CoverageConventer
