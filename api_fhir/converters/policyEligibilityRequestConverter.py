from policy.services import ByInsureeRequest

from api_fhir.configurations import Stu3EligibilityConfiguration as Config
from api_fhir.converters import BaseFHIRConverter, PatientConverter, ContractConverter
from api_fhir.models import EligibilityResponse as FHIREligibilityResponse, InsuranceBenefitBalance, \
    EligibilityResponseInsurance, InsuranceBenefitBalanceFinancial, Money, Reference, \
    Identifier


class PolicyEligibilityRequestConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, eligibility_response):
        fhir_response = FHIREligibilityResponse()
        for item in eligibility_response.items:
            if item.status in Config.get_fhir_active_policy_status():
                cls.build_fhir_insurance(fhir_response, item)
        return fhir_response

    @classmethod
    def to_imis_obj(cls, fhir_eligibility_request, audit_user_id):
        uuid = cls.build_imis_uuid(fhir_eligibility_request)
        return ByInsureeRequest(uuid)

    @classmethod
    def build_fhir_insurance(cls, fhir_response, response):
        result = EligibilityResponseInsurance()
        cls.build_fhir_insurance_contract(result, response)
        cls.build_fhir_money_benefit(result, Config.get_fhir_balance_code(),
                                     response.ceiling,
                                     response.ded)
        fhir_response.insurance.append(result)

    @classmethod
    def build_fhir_insurance_contract(cls, insurance, contract):
        insurance.contract = ContractConverter.build_fhir_resource_reference(
            contract)

    @classmethod
    def build_fhir_money_benefit(cls, insurance, code, allowed_value, used_value):
        benefit_balance = cls.build_fhir_generic_benefit_balance(code)
        cls.build_fhir_money_benefit_balance_financial(
            benefit_balance, allowed_value, used_value)
        insurance.benefitBalance.append(benefit_balance)

    @classmethod
    def build_fhir_generic_benefit_balance(cls, code):
        benefit_balance = InsuranceBenefitBalance()
        benefit_balance.category = cls.build_simple_codeable_concept(
            Config.get_fhir_balance_default_category())
        return benefit_balance

    @classmethod
    def build_fhir_money_benefit_balance_financial(cls, benefit_balance, allowed_value, used_value):
        financial = cls.build_fhir_generic_benefit_balance_financial()
        allowed_money_value = Money()
        allowed_money_value.value = allowed_value or 0
        financial.allowedMoney = allowed_money_value
        used_money_value = Money()
        used_money_value.value = used_value or 0
        financial.usedMoney = used_money_value
        benefit_balance.financial.append(financial)

    @classmethod
    def build_fhir_generic_benefit_balance_financial(cls):
        financial = InsuranceBenefitBalanceFinancial()
        financial.type = cls.build_simple_codeable_concept(
            Config.get_fhir_financial_code())
        return financial

    @classmethod
    def build_imis_uuid(cls, fhir_eligibility_request):
        uuid = None
        patient_reference = fhir_eligibility_request.patient
        if patient_reference:
            uuid = PatientConverter.get_resource_id_from_reference(
                patient_reference)
        return uuid
