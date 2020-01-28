from api_fhir.configurations import Stu3CoverageConfig
from api_fhir.converters import BaseFHIRConverter, PractitionerConverter
from api_fhir.models import Coverage, Reference, Period, Contract, ContractValuedItem, Money, CoverageGrouping, \
    ContractAgent, Extension
from product.models import ProductItem, ProductService


class CoverageConventer(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_policy):
        fhir_coverage = Coverage()
        cls.build_coverage_identifier(fhir_coverage, imis_policy)
        cls.build_coverage_policy_holder(fhir_coverage, imis_policy)
        cls.build_coverage_period(fhir_coverage, imis_policy)
        cls.build_coverage_status(fhir_coverage, imis_policy)
        cls.build_coverage_contract(fhir_coverage, imis_policy)
        cls.build_coverage_grouping(fhir_coverage, imis_policy)
        cls.build_coverage_extension(fhir_coverage, imis_policy)
        return fhir_coverage

    @classmethod
    def build_coverage_identifier(cls, fhir_coverage, imis_policy):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_policy)
        fhir_coverage.identifier = identifiers
        return fhir_coverage

    @classmethod
    def build_coverage_policy_holder(cls, fhir_coverage, imis_policy):
        reference = Reference()
        resource_type = Stu3CoverageConfig.get_family_reference_code()
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
        cls.build_contract_agent(contract, imis_coverage)
        fhir_coverage.contract.append(contract)
        return fhir_coverage

    @classmethod
    def build_contract_valued_item(self, contract, imis_coverage):
        valued_item = ContractValuedItem()
        policy_value = Money()
        policy_value.value = imis_coverage.value
        valued_item.net = policy_value
        contract.valuedItem = [valued_item]
        return contract

    @classmethod
    def build_contract_agent(cls, contract, imis_coverage):
        agent = ContractAgent()
        actor = PractitionerConverter.build_fhir_resource_reference(imis_coverage.officer)
        agent.actor = actor
        provider_role = cls.build_simple_codeable_concept(Stu3CoverageConfig.get_practitioner_role_code())
        agent.role = [provider_role]
        contract.agent = [agent]

    @classmethod
    def build_coverage_grouping(cls, fhir_coverage, imis_coverage):
        grouping = CoverageGrouping()
        product = imis_coverage.product
        grouping.group = Stu3CoverageConfig.get_product_code() + "/" + str(product.uuid)
        grouping.groupDisplay = product.code

        cls.__build_product_plan_display(grouping, product)
        fhir_coverage.grouping = grouping

    @classmethod
    def __map_status(cls, code):
        codes = {
            1: Stu3CoverageConfig.get_status_idle_code(),
            2: Stu3CoverageConfig.get_status_active_code(),
            4: Stu3CoverageConfig.get_status_suspended_code(),
            8: Stu3CoverageConfig.get_status_expired_code(),
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
                                                 Stu3CoverageConfig.get_effective_date_code())
        fhir_coverage.extension.append(enroll_date)

    @classmethod
    def __build_enroll_date(cls, fhir_coverage, imis_coverage):
        enroll_date = cls.__build_date_extension(imis_coverage.enroll_date,
                                                 Stu3CoverageConfig.get_enroll_date_code())
        fhir_coverage.extension.append(enroll_date)

    @classmethod
    def __build_date_extension(cls, value, name):
        ext_date = Extension()
        ext_date.url = name
        ext_date.valueDate = value.isoformat() if value else None
        return ext_date

    @classmethod
    def __build_product_plan_display(cls, grouping, product):
        product_coverage = {}
        service_code = Stu3CoverageConfig.get_service_code()
        item_code = Stu3CoverageConfig.get_item_code()
        product_items = ProductItem.objects.filter(product=product).all()
        product_services = ProductService.objects.filter(product=product).all()

        product_coverage[item_code] = [item.item.code for item in product_items]
        product_coverage[service_code] = [service.service.code for service in product_services]
        grouping.plan = product.name
        grouping.planDisplay = str(product_coverage)
