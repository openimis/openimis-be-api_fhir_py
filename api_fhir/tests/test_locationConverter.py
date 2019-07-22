import os

from api_fhir.converters.locationConverter import LocationConverter
from api_fhir.models import FHIRBaseObject
from api_fhir.tests import LocationTestMixin


class LocationConverterTestCase(LocationTestMixin):

    __TEST_LOCATION_JSON_PATH = "/test/test_location.json"

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_location_json_representation = open(dir_path + self.__TEST_LOCATION_JSON_PATH).read()

    def test_to_fhir_obj(self):
        imis_hf = self.create_test_imis_instance()
        fhir_location = LocationConverter.to_fhir_obj(imis_hf)
        self.verify_fhir_instance(fhir_location)

    def test_to_imis_obj(self):
        fhir_loaction = self.create_test_fhir_instance()
        imis_hf = LocationConverter.to_imis_obj(fhir_loaction, None)
        self.verify_imis_instance(imis_hf)

    def test_create_object_from_json(self):
        self.setUp()
        fhir_location = FHIRBaseObject.loads(self._test_location_json_representation, 'json')
        self.verify_fhir_instance(fhir_location)

    def test_fhir_object_to_json(self):
        self.setUp()
        fhir_location = self.create_test_fhir_instance()
        actual_representation = fhir_location.dumps(format_='json')
        self.assertEqual(self._test_location_json_representation, actual_representation)
