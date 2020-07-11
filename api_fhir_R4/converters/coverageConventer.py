from api_fhir_R4.configurations import R4CoverageConfig
from api_fhir_R4.converters import BaseFHIRConverter, PractitionerConverter, ReferenceConverterMixin
from api_fhir_R4.models import Coverage, Reference, Period, Contract, Money, Extension, ContractTermAssetValuedItem, \
    ContractTermOfferParty, CoverageClass
from product.models import ProductItem, ProductService
from policy.models import Policy
from api_fhir_R4.utils import DbManagerUtils


class CoverageConventer(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_policy):
        fhir_coverage = Coverage()
        cls.build_coverage_identifier(fhir_coverage, imis_policy)
        cls.build_coverage_policy_holder(fhir_coverage, imis_policy)
        cls.build_coverage_period(fhir_coverage, imis_policy)
        cls.build_coverage_status(fhir_coverage, imis_policy)
        cls.build_coverage_contract(fhir_coverage, imis_policy)
        cls.build_coverage_class(fhir_coverage, imis_policy)
        cls.build_coverage_extension(fhir_coverage, imis_policy)
        return fhir_coverage

    @classmethod
    def get_reference_obj_id(cls, imis_policy):
        return imis_policy.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return Coverage

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_policy_code = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(Policy, code=imis_policy_code)

    @classmethod
    def build_coverage_identifier(cls, fhir_coverage, imis_policy):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_policy)
        fhir_coverage.identifier = identifiers
        return fhir_coverage

    @classmethod
    def build_coverage_policy_holder(cls, fhir_coverage, imis_policy):
        reference = Reference()
        resource_type = R4CoverageConfig.get_family_reference_code()
        resource_id = imis_policy.family.uuid
        reference.reference = resource_type + '/' + str(resource_id)
        fhir_coverage.policyHolder = reference
        return fhir_coverage

    @classmethod
    def build_coverage_period(cls, fhir_coverage, imis_policy):
        period = Period()
        period.start = imis_policy.start_date.isoformat()
        period.end = imis_policy.expiry_date.isoformat()
        fhir_coverage.period = period
        return period

    @classmethod
    def build_coverage_status(cls, fhir_coverage, imis_policy):
        code = imis_policy.status
        fhir_coverage.status = cls.__map_status(code)
        return fhir_coverage

    @classmethod
    def build_coverage_contract(cls, fhir_coverage, imis_coverage):
        contract = Contract()
        cls.build_contract_valued_item(contract, imis_coverage)
        cls.build_contract_party(contract, imis_coverage)
        fhir_coverage.contract.append(contract)
        return fhir_coverage

    @classmethod
    def build_contract_valued_item(self, contract, imis_coverage):
        valued_item = ContractTermAssetValuedItem()
        policy_value = Money()
        policy_value.value = imis_coverage.value
        valued_item.net = policy_value
        contract.term[0].asset[0].valuedItem[0] = [valued_item]
        return contract

    @classmethod
    def build_contract_party(cls, contract, imis_coverage):
        party = ContractTermOfferParty()
        reference = PractitionerConverter.build_fhir_resource_reference(imis_coverage.officer)
        party.reference = reference
        provider_role = cls.build_simple_codeable_concept(R4CoverageConfig.get_practitioner_role_code())
        party.role = [provider_role]
        contract.term[0].offer[0].party[0] = [party]

    @classmethod
    def build_coverage_class(cls, fhir_coverage, imis_coverage):
        class_ = CoverageClass()
        product = imis_coverage.product
        class_.type = R4CoverageConfig.get_product_code() + "/" + str(product.uuid)
        class_.name = product.code

        cls.__build_product_plan_display(class_, product)
        fhir_coverage.class_[0] = class_

    @classmethod
    def __map_status(cls, code):
        codes = {
            1: R4CoverageConfig.get_status_idle_code(),
            2: R4CoverageConfig.get_status_active_code(),
            4: R4CoverageConfig.get_status_suspended_code(),
            8: R4CoverageConfig.get_status_expired_code(),
        }
        return codes[code]

    @classmethod
    def build_coverage_extension(cls, fhir_coverage, imis_coverage):
        cls.__build_effective_date(fhir_coverage, imis_coverage)
        cls.__build_enroll_date(fhir_coverage, imis_coverage)
        return fhir_coverage

    @classmethod
    def __build_effective_date(cls, fhir_coverage, imis_coverage):
        enroll_date = cls.__build_date_extension(imis_coverage.effective_date,
                                                 R4CoverageConfig.get_effective_date_code())
        fhir_coverage.extension.append(enroll_date)

    @classmethod
    def __build_enroll_date(cls, fhir_coverage, imis_coverage):
        enroll_date = cls.__build_date_extension(imis_coverage.enroll_date,
                                                 R4CoverageConfig.get_enroll_date_code())
        fhir_coverage.extension.append(enroll_date)

    @classmethod
    def __build_date_extension(cls, value, name):
        ext_date = Extension()
        ext_date.url = name
        ext_date.valueDate = value.isoformat() if value else None
        return ext_date

    @classmethod
    def __build_product_plan_display(cls, class_, product):
        product_coverage = {}
        service_code = R4CoverageConfig.get_service_code()
        item_code = R4CoverageConfig.get_item_code()
        product_items = ProductItem.objects.filter(product=product).all()
        product_services = ProductService.objects.filter(product=product).all()

        product_coverage[item_code] = [item.item.code for item in product_items]
        product_coverage[service_code] = [service.service.code for service in product_services]
        class_.type = product.name
        class_.name = str(product_coverage)
