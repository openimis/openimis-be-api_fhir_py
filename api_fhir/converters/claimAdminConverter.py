from api_fhir.converters import BaseFHIRConverter


class ClaimAdminConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, obj):
        pass  # TODO need to be added

    @classmethod
    def to_imis_obj(cls, data, audit_user_id):
        pass  # TODO need to be added

    class Meta:
        app_label = 'api_fhir'
