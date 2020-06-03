from api_fhir_R4.models import Contract

from api_fhir_R4.converters import BaseFHIRConverter, ReferenceConverterMixin


class ContractConverter(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def get_reference_obj_id(cls, imis_contract):
        return f'{imis_contract.product_code}/{imis_contract.expiry_date}'

    @classmethod
    def get_fhir_resource_type(cls):
        return Contract
