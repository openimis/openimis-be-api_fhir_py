from policy.services import EligibilityRequest

from api_fhir.configurations import Stu3EligibilityConfiguration as Config
from api_fhir.converters import BaseFHIRConverter, PatientConverter
from api_fhir.models import EligibilityResponse as FHIREligibilityResponse, InsuranceBenefitBalance, \
    EligibilityResponseInsurance, InsuranceBenefitBalanceFinancial, Money


class EligibilityRequestConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, eligibility_response):
        fhir_response = FHIREligibilityResponse()
        cls.build_fhir_insurance(fhir_response, eligibility_response)
        return fhir_response

    @classmethod
    def to_imis_obj(cls, fhir_eligibility_request, audit_user_id):
        uuid = cls.build_imis_uuid(fhir_eligibility_request)
        service_code = cls.build_imis_service_code(fhir_eligibility_request)
        item_code = cls.build_imis_item_code(fhir_eligibility_request)
        return EligibilityRequest(uuid, service_code, item_code)

    @classmethod
    def build_fhir_insurance(cls, fhir_response, response):
        result = EligibilityResponseInsurance()
        cls.build_fhir_int_benefit(result, Config.get_fhir_total_admissions_code(), response.total_admissions_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_total_visits_code(), response.total_visits_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_total_consultations_code(),
                                   response.total_consultations_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_total_surgeries_code(), response.total_surgeries_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_total_deliveries_code(), response.total_deliveries_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_total_antenatal_code(), response.total_antenatal_left)
        cls.build_fhir_money_benefit(result, Config.get_fhir_consultation_amount_code(),
                                     response.consultation_amount_left)
        cls.build_fhir_money_benefit(result, Config.get_fhir_surgery_amount_code(), response.surgery_amount_left)
        cls.build_fhir_money_benefit(result, Config.get_fhir_delivery_amount_code(), response.delivery_amount_left)
        cls.build_fhir_money_benefit(result, Config.get_fhir_hospitalization_amount_code(),
                                     response.hospitalization_amount_left)
        cls.build_fhir_money_benefit(result, Config.get_fhir_antenatal_amount_code(), response.antenatal_amount_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_service_left_code(), response.service_left)
        cls.build_fhir_int_benefit(result, Config.get_fhir_item_left_code(), response.item_left)
        cls.build_fhir_bool_benefit(result, Config.get_fhir_is_service_ok_code(), response.is_service_ok)
        cls.build_fhir_bool_benefit(result, Config.get_fhir_is_item_ok_code(), response.is_item_ok)
        fhir_response.insurance.append(result)

    @classmethod
    def build_fhir_bool_benefit(cls, insurance, code, is_ok):
        if is_ok is not None:
            benefit_balance = cls.build_fhir_generic_benefit_balance(code)
            benefit_balance.excluded = not is_ok
            insurance.benefitBalance.append(benefit_balance)

    @classmethod
    def build_fhir_int_benefit(cls, insurance, code, value):
        if value is not None:
            benefit_balance = cls.build_fhir_generic_benefit_balance(code)
            cls.build_fhir_int_benefit_balance_financial(benefit_balance, value)
            insurance.benefitBalance.append(benefit_balance)

    @classmethod
    def build_fhir_money_benefit(cls, insurance, code, value):
        if value is not None:
            benefit_balance = cls.build_fhir_generic_benefit_balance(code)
            cls.build_fhir_money_benefit_balance_financial(benefit_balance, value)
            insurance.benefitBalance.append(benefit_balance)

    @classmethod
    def build_fhir_generic_benefit_balance(cls, code):
        benefit_balance = InsuranceBenefitBalance()
        benefit_balance.category = cls.build_simple_codeable_concept(code)
        return benefit_balance

    @classmethod
    def build_fhir_int_benefit_balance_financial(cls, benefit_balance, value):
        financial = cls.build_fhir_generic_benefit_balance_financial()
        financial.allowedUnsignedInt = value
        benefit_balance.financial.append(financial)

    @classmethod
    def build_fhir_money_benefit_balance_financial(cls, benefit_balance, value):
        financial = cls.build_fhir_generic_benefit_balance_financial()
        money_value = Money()
        money_value.value = value
        financial.allowedMoney = money_value
        benefit_balance.financial.append(financial)

    @classmethod
    def build_fhir_generic_benefit_balance_financial(cls):
        financial = InsuranceBenefitBalanceFinancial()
        financial.type = cls.build_simple_codeable_concept(Config.get_fhir_financial_code())
        return financial

    @classmethod
    def build_imis_uuid(cls, fhir_eligibility_request):
        uuid = None
        patient_reference = fhir_eligibility_request.patient
        if patient_reference:
            uuid = PatientConverter.get_resource_id_from_reference(patient_reference)
        return uuid

    @classmethod
    def build_imis_service_code(cls, fhir_eligibility_request):
        return cls.get_text_from_codeable_concept_by_coding_code(fhir_eligibility_request.benefitCategory,
                                                                 Config.get_fhir_service_code())

    @classmethod
    def build_imis_item_code(cls, fhir_eligibility_request):
        return cls.get_text_from_codeable_concept_by_coding_code(fhir_eligibility_request.benefitSubCategory,
                                                                 Config.get_fhir_item_code())

    @classmethod
    def get_text_from_codeable_concept_by_coding_code(cls, codeable_concept, coding_code):
        service_code = None
        if codeable_concept:
            coding = cls.get_first_coding_from_codeable_concept(codeable_concept)
            if coding and coding.code == coding_code:
                service_code = codeable_concept.text
        return service_code
