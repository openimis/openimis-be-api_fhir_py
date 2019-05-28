from api_fhir.converters import BaseFHIRConverter


class LocationConverter(BaseFHIRConverter):
    @classmethod
    def to_fhir_obj(cls, obj):
        pass


    @classmethod
    def to_imis_obj(cls, data, audit_user_id):
        pass