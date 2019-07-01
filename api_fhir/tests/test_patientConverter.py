import os

from api_fhir.converters import PatientConverter

from api_fhir.models import FHIRBaseObject
from mixin.patientTestMixin import PatientTestMixin


class PatientConverterTestCase(PatientTestMixin):

    __TEST_PATIENT_JSON_PATH = "/test/test_patient.json"

    def __set_up(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_patient_json_representation = open(dir_path + self.__TEST_PATIENT_JSON_PATH).read()

    def test_to_fhir_obj(self):
        self.__set_up()
        imis_insuree = self.create_test_imis_instance()
        fhir_patient = PatientConverter.to_fhir_obj(imis_insuree)
        self.verify_fhir_instance(fhir_patient)

    def test_to_imis_obj(self):
        self.__set_up()
        fhir_patient = self.create_test_fhir_instance()
        imis_insuree = PatientConverter.to_imis_obj(fhir_patient, None)
        self.verify_imis_instance(imis_insuree)

    def test_create_object_from_json(self):
        self.__set_up()
        fhir_patient = FHIRBaseObject.loads(self._test_patient_json_representation, 'json')
        self.verify_fhir_instance(fhir_patient)

    def test_fhir_object_to_json(self):
        self.__set_up()
        fhir_patient = self.create_test_fhir_instance()
        self.add_imis_db_id_to_fhir_resource(fhir_patient)
        actual_representation = fhir_patient.dumps(format_='json')
        self.assertEqual(self._test_patient_json_representation, actual_representation)
