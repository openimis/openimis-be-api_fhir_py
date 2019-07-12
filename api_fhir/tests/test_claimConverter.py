from unittest import mock

from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.tests import ClaimTestMixin


class ClaimConverterTestCase(ClaimTestMixin):

    def set_up(self):
        super(ClaimConverterTestCase, self).set_up()

    def test_to_fhir_obj(self):
        imis_claim = self.create_test_imis_instance()
        fhir_claim = ClaimConverter.to_fhir_obj(imis_claim)
        self.verify_fhir_instance(fhir_claim)

    @mock.patch('location.models.HealthFacility.objects')
    @mock.patch('claim.models.ClaimAdmin.objects')
    @mock.patch('claim.models.ClaimDiagnosisCode.objects')
    @mock.patch('insuree.models.Insuree.objects')
    def test_to_imis_obj(self, mock_insuree, mock_cdc, mock_ca, mock_hf):
        self.set_up()
        mock_insuree.filter().first.return_value = self._TEST_INSUREE
        mock_cdc.get.return_value = self._TEST_DIAGNOSIS_CODE
        mock_ca.filter().first.return_value = self._TEST_CLAIM_ADMIN
        mock_hf.filter().first.return_value = self._TEST_HF

        fhir_claim = self.create_test_fhir_instance()
        imis_claim = ClaimConverter.to_imis_obj(fhir_claim, None)
        self.verify_imis_instance(imis_claim)
