import os
from unittest import mock

from api_fhir.converters import LocationConverter, PatientConverter, PractitionerConverter
from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.models import FHIRBaseObject
from api_fhir.tests import ClaimTestMixin


class ClaimConverterTestCase(ClaimTestMixin):

    __TEST_CLAIM_JSON_PATH = "/test/test_claim.json"

    def setUp(self):
        super(ClaimConverterTestCase, self).setUp()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_claim_json_representation = open(dir_path + self.__TEST_CLAIM_JSON_PATH).read()
        if self._test_claim_json_representation[-1:] == "\n":
            self._test_claim_json_representation = self._test_claim_json_representation[:-1]

    @mock.patch('claim.models.ClaimItem.objects')
    @mock.patch('claim.models.ClaimService.objects')
    def test_to_fhir_obj(self, cs_mock, ci_mock):
        cs_mock.filter.return_value = [self._TEST_SERVICE]
        ci_mock.filter.return_value = [self._TEST_ITEM]

        imis_claim = self.create_test_imis_instance()
        fhir_claim = ClaimConverter.to_fhir_obj(imis_claim)
        self.verify_fhir_instance(fhir_claim)

    @mock.patch.object(LocationConverter, 'get_imis_obj_by_fhir_reference')
    @mock.patch.object(PractitionerConverter, 'get_imis_obj_by_fhir_reference')
    @mock.patch('medical.models.Diagnosis.objects')
    @mock.patch.object(PatientConverter, 'get_imis_obj_by_fhir_reference')
    def test_to_imis_obj(self, mock_insuree, mock_cdc, mock_pc, mock_hfc):
        self.setUp()
        mock_insuree.return_value = self._TEST_INSUREE
        mock_cdc.get.return_value = self._TEST_DIAGNOSIS_CODE
        mock_pc.return_value = self._TEST_CLAIM_ADMIN
        mock_hfc.return_value = self._TEST_HF

        fhir_claim = self.create_test_fhir_instance()
        imis_claim = ClaimConverter.to_imis_obj(fhir_claim, None)
        self.verify_imis_instance(imis_claim)

    def test_fhir_object_to_json_request(self):
        self.setUp()
        fhir_obj = self.create_test_fhir_instance()
        actual_representation = fhir_obj.dumps(format_='json')
        self.assertEqual(self._test_claim_json_representation, actual_representation)

    def test_create_object_from_json(self):
        self.setUp()
        fhir_claim = FHIRBaseObject.loads(self._test_claim_json_representation, 'json')
        self.verify_fhir_instance(fhir_claim)
