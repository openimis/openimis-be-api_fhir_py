import os

from api_fhir.converters import PractitionerConverter

from api_fhir.models import FHIRBaseObject
from api_fhir.tests import PractitionerTestMixin


class PractitionerConverterTestCase(PractitionerTestMixin):

    __TEST_PRACTITIONER_JSON_PATH = "/test/test_practitioner.json"

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_practitioner_json_representation = open(dir_path + self.__TEST_PRACTITIONER_JSON_PATH).read()

    def test_to_fhir_obj(self):
        imis_claim_admin = self.create_test_imis_instance()
        fhir_practitioner = PractitionerConverter.to_fhir_obj(imis_claim_admin)
        self.verify_fhir_instance(fhir_practitioner)

    def test_to_imis_obj(self):
        fhir_practitioner = self.create_test_fhir_instance()
        imis_claim_admin = PractitionerConverter.to_imis_obj(fhir_practitioner, None)
        self.verify_imis_instance(imis_claim_admin)

    def test_create_object_from_json(self):
        self.setUp()
        fhir_practitioner = FHIRBaseObject.loads(self._test_practitioner_json_representation, 'json')
        self.verify_fhir_instance(fhir_practitioner)

    def test_fhir_object_to_json(self):
        self.setUp()
        fhir_practitioner = self.create_test_fhir_instance()
        actual_representation = fhir_practitioner.dumps(format_='json')
        self.assertEqual(self._test_practitioner_json_representation, actual_representation)
