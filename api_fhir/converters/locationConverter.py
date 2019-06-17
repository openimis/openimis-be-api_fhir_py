from location.models import HealthFacility

from api_fhir.apiFhirConfiguration import ApiFhirConfiguration
from api_fhir.converters import BaseFHIRConverter
from api_fhir.models import Location, ContactPointSystem, ContactPointUse
from api_fhir.models.address import AddressUse, AddressType
from api_fhir.models.imisModelEnums import ImisHfLevel
import core

class LocationConverter(BaseFHIRConverter):
    @classmethod
    def to_fhir_obj(cls, imis_hf):
        fhir_location = Location()
        cls.build_fhir_location_identifier(fhir_location, imis_hf)
        cls.build_fhir_location_name(fhir_location, imis_hf)
        cls.build_fhir_location_type(fhir_location, imis_hf)
        cls.build_fhir_location_address(fhir_location, imis_hf)
        cls.build_fhir_location_telcome(fhir_location, imis_hf)
        return fhir_location

    @classmethod
    def to_imis_obj(cls, fhir_location, audit_user_id):
        errors = []
        imis_hf = cls.createDefaultInsuree(audit_user_id)
        cls.build_imis_hf_identiftier(imis_hf, fhir_location, errors)
        cls.build_imis_hf_name(imis_hf, fhir_location, errors)
        cls.build_imis_hf_level(imis_hf, fhir_location, errors)
        cls.build_imis_hf_address(imis_hf, fhir_location)
        cls.build_imis_hf_contacts(imis_hf, fhir_location)
        cls.check_errors(errors)
        return imis_hf

    @classmethod
    def createDefaultInsuree(cls, audit_user_id):
        imis_hf = HealthFacility()
        # TODO legalForm isn't covered because that value is missing in the model (value need to be nullable in DB)
        # TODO LocationId isn't covered because that value is missing in the model (value need to be nullable in DB)
        imis_hf.offline = ApiFhirConfiguration.get_default_value_of_location_offline_attribute()
        imis_hf.care_type = ApiFhirConfiguration.get_default_value_of_location_care_type()
        imis_hf.validity_from = core.datetime.datetime.now()
        imis_hf.audit_user_id = audit_user_id
        return imis_hf

    @classmethod
    def build_fhir_location_identifier(cls, fhir_location, imis_hf):
        identifiers = []
        cls.build_fhir_id_identifier(identifiers, imis_hf)
        cls.build_fhir_hf_code_identifier(identifiers, imis_hf)
        fhir_location.identifier = identifiers

    @classmethod
    def build_fhir_hf_code_identifier(cls, identifiers, imis_hf):
        if imis_hf is not None:
            identifier = cls.build_fhir_identifier(imis_hf.code,
                                                   ApiFhirConfiguration.get_fhir_identifier_type_system(),
                                                   ApiFhirConfiguration.get_fhir_facility_id_type())
            identifiers.append(identifier.__dict__)

    @classmethod
    def build_imis_hf_identiftier(cls, imis_hf, fhir_location, errors):
        if fhir_location.get('identifier') is not None:
            for identifier in fhir_location.get('identifier'):
                identifier_type = identifier.get("type")
                if identifier_type is not None \
                        and identifier_type.get('coding') is not None \
                        and identifier_type.get('coding')[0].get("system") == ApiFhirConfiguration \
                        .get_fhir_identifier_type_system():
                    if identifier_type.get('coding')[0].get("code") == ApiFhirConfiguration.get_fhir_facility_id_type():
                        if identifier.get("value") is not None:
                            imis_hf.code = identifier.get("value")
        cls.valid_condition(imis_hf.code is None, 'Missing hf code', errors)

    @classmethod
    def build_fhir_location_name(cls, fhir_location, imis_hf):
        fhir_location.name = imis_hf.name

    @classmethod
    def build_imis_hf_name(cls, imis_hf, fhir_location, errors):
        if not cls.valid_condition(fhir_location.get('name') is None,
                                   'Missing patient `name` attribute', errors):
            imis_hf.name = fhir_location.get('name')

    @classmethod
    def build_fhir_location_type(cls, fhir_location, imis_hf):
        code = ""
        if imis_hf.level == ImisHfLevel.HEALTH_CENTER.value:
            code = ApiFhirConfiguration.get_fhir_code_for_health_center()
        elif imis_hf.level == ImisHfLevel.HOSPITAL.value:
            code = ApiFhirConfiguration.get_fhir_code_for_hospital()
        elif imis_hf.level == ImisHfLevel.DISPENSARY.value:
            code = ApiFhirConfiguration.get_fhir_code_for_dispensary()

        fhir_location.type = \
            cls.build_codeable_concept(code, ApiFhirConfiguration.get_fhir_location_role_type_system()).__dict__

    @classmethod
    def build_imis_hf_level(cls, imis_hf, fhir_location, errors):
        if not cls.valid_condition(fhir_location.get('type') is None,
                                   'Missing patient `type` attribute', errors):
            for maritialCoding in fhir_location.get('type').get('coding'):
                if maritialCoding.get("system") == ApiFhirConfiguration.get_fhir_location_role_type_system():
                    code = maritialCoding.get("code")
                    if code == ApiFhirConfiguration.get_fhir_code_for_health_center():
                        imis_hf.level = ImisHfLevel.HEALTH_CENTER.value
                    elif code == ApiFhirConfiguration.get_fhir_code_for_hospital():
                        imis_hf.level = ImisHfLevel.HOSPITAL.value
                    elif code == ApiFhirConfiguration.get_fhir_code_for_dispensary():
                        imis_hf.level = ImisHfLevel.DISPENSARY.value

            cls.valid_condition(imis_hf.level is None, 'Missing hf level', errors)

    @classmethod
    def build_fhir_location_address(cls, fhir_location, imis_hf):
        fhir_location.address = cls.build_fhir_address(imis_hf.address, AddressUse.HOME.value,
                                                       AddressType.PHYSICAL.value).__dict__

    @classmethod
    def build_imis_hf_address(cls, imis_hf, fhir_location):
        address = fhir_location.get('address')
        if address is not None:
            if address.get("type") == AddressType.PHYSICAL.value:
                imis_hf.address = address.get("text")

    @classmethod
    def build_fhir_location_telcome(cls, fhir_location, imis_hf):
        telecom = []
        if imis_hf.phone is not None:
            phone = LocationConverter.build_fhir_contact_point(imis_hf.phone, ContactPointSystem.PHONE.value,
                                                               ContactPointUse.HOME.value)
            telecom.append(phone.__dict__)
        if imis_hf.fax is not None:
            fax = LocationConverter.build_fhir_contact_point(imis_hf.fax, ContactPointSystem.FAX.value,
                                                             ContactPointUse.HOME.value)
            telecom.append(fax.__dict__)
        if imis_hf.email is not None:
            email = LocationConverter.build_fhir_contact_point(imis_hf.email, ContactPointSystem.EMAIL.value,
                                                               ContactPointUse.HOME.value)
            telecom.append(email.__dict__)
        fhir_location.telecom = telecom

    @classmethod
    def build_imis_hf_contacts(cls, imis_hf, fhir_location):
        if fhir_location.get('telecom') is not None:
            for contact_point in fhir_location.get('telecom'):
                if contact_point.get("system") == ContactPointSystem.PHONE.value:
                    imis_hf.phone = contact_point.get("value")
                elif contact_point.get("system") == ContactPointSystem.FAX.value:
                    imis_hf.fax = contact_point.get("value")
                elif contact_point.get("system") == ContactPointSystem.EMAIL.value:
                    imis_hf.email = contact_point.get("value")

    class Meta:
        app_label = 'api_fhir'
