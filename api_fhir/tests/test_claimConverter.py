from api_fhir.converters.claimConverter import ClaimConverter
from mixin.claimTestMixin import ClaimTestMixin


class ClaimConverterTestCase(ClaimTestMixin):

    def test_to_fhir_obj(self):
        imis_claim = self.create_test_imis_instance()
        fhir_claim = ClaimConverter.to_fhir_obj(imis_claim)
        self.verify_fhir_instance(fhir_claim)

    def test_to_imis_obj(self):
        fhir_claim = self.create_test_fhir_instance()
        imis_claim = ClaimConverter.to_imis_obj(fhir_claim, None)
        self.verify_imis_instance(imis_claim)
