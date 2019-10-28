from abc import ABC

from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.exceptions import FHIRRequestProcessException
from api_fhir.models import CodeableConcept, ContactPoint, Address, Coding, Identifier, IdentifierUse


class BaseFHIRConverter(ABC):

    @classmethod
    def to_fhir_obj(cls, obj):
        raise NotImplementedError('`toFhirObj()` must be implemented.')  # pragma: no cover

    @classmethod
    def to_imis_obj(cls, data, audit_user_id):
        raise NotImplementedError('`toImisObj()` must be implemented.')  # pragma: no cover

    @classmethod
    def build_fhir_pk(cls, fhir_obj, resource_id):
        fhir_obj.id = resource_id

    @classmethod
    def valid_condition(cls, condition, error_message, errors=None):
        if errors is None:
            errors = []
        if condition:
            errors.append(error_message)
        return condition

    @classmethod
    def check_errors(cls, errors=None):  # pragma: no cover
        if errors is None:
            errors = []
        if len(errors) > 0:
            raise FHIRRequestProcessException(errors)

    @classmethod
    def build_simple_codeable_concept(cls, text):
        return cls.build_codeable_concept(None, None, text)

    @classmethod
    def build_codeable_concept(cls, code, system=None, text=None):
        codeable_concept = CodeableConcept()
        if code or system:
            coding = Coding()
            coding.system = system
            if not isinstance(code, str):
                code = str(code)
            coding.code = code
            codeable_concept.coding = [coding]
        codeable_concept.text = text
        return codeable_concept

    @classmethod
    def get_first_coding_from_codeable_concept(cls, codeable_concept):
        result = Coding()
        if codeable_concept:
            coding = codeable_concept.coding
            if coding and isinstance(coding, list) and len(coding) > 0:
                result = codeable_concept.coding[0]
        return result

    @classmethod
    def build_fhir_uuid_identifier(cls, identifiers, imis_object):
        if imis_object.uuid is not None:
            identifier = cls.build_fhir_identifier(imis_object.uuid,
                                                   Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                   Stu3IdentifierConfig.get_fhir_uuid_type_code())
            identifiers.append(identifier)

    @classmethod
    def build_fhir_identifier(cls, value, type_system, type_code):
        identifier = Identifier()
        identifier.use = IdentifierUse.USUAL.value
        type = cls.build_codeable_concept(type_code, type_system)
        identifier.type = type
        identifier.value = value
        return identifier

    @classmethod
    def get_fhir_identifier_by_code(cls, identifiers, lookup_code):
        value = None
        for identifier in identifiers or []:
            first_coding = cls.get_first_coding_from_codeable_concept(identifier.type)
            if first_coding.system == Stu3IdentifierConfig.get_fhir_identifier_type_system() \
                    and first_coding.code == lookup_code:
                    value = identifier.value
                    break
        return value

    @classmethod
    def build_fhir_contact_point(cls, value, contact_point_system, contact_point_use):
        contact_point = ContactPoint()
        contact_point.system = contact_point_system
        contact_point.use = contact_point_use
        contact_point.value = value
        return contact_point

    @classmethod
    def build_fhir_address(cls, value, use, type):
        current_address = Address()
        current_address.text = value
        current_address.use = use
        current_address.type = type
        return current_address


from api_fhir.converters.personConverterMixin import PersonConverterMixin
from api_fhir.converters.referenceConverterMixin import ReferenceConverterMixin
from api_fhir.converters.contractConverter import ContractConverter
from api_fhir.converters.patientConverter import PatientConverter
from api_fhir.converters.locationConverter import LocationConverter
from api_fhir.converters.operationOutcomeConverter import OperationOutcomeConverter
from api_fhir.converters.practitionerConverter import PractitionerConverter
from api_fhir.converters.practitionerRoleConverter import PractitionerRoleConverter
from api_fhir.converters.eligibilityRequestConverter import EligibilityRequestConverter
from api_fhir.converters.policyEligibilityRequestConverter import PolicyEligibilityRequestConverter
from api_fhir.converters.communicationRequestConverter import CommunicationRequestConverter
from api_fhir.converters.claimResponseConverter import ClaimResponseConverter
