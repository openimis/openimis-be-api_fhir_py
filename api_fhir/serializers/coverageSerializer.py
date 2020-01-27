from api_fhir.converters.coverageConventer import CoverageConventer
from api_fhir.serializers import BaseFHIRSerializer


class CoverageSerializer(BaseFHIRSerializer):

    fhirConverter = CoverageConventer
