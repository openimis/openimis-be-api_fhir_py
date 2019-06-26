from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.converters import BaseFHIRConverter


class DbIdTestMixin(object):

    def get_test_db_id(self):
        raise NotImplementedError('`test_imis_instance()` must be implemented.')

    def add_imis_db_id_to_fhir_resource(self, fhir_obj, db_id=None):
        if not db_id:
            db_id = self.get_test_db_id()
        location_id = BaseFHIRConverter.build_fhir_identifier(db_id,
                                                              Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                              Stu3IdentifierConfig.get_fhir_id_type_code())
        fhir_obj.identifier.append(location_id)
