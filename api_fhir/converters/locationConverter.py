from django.utils.translation import gettext
from location.models import HealthFacility

from api_fhir.configurations import GeneralConfiguration, Stu3IdentifierConfig, Stu3LocationConfig
from api_fhir.converters import BaseFHIRConverter, ReferenceConverterMixin
from api_fhir.models import Location, ContactPointSystem, ContactPointUse
from api_fhir.models.address import AddressUse, AddressType
from api_fhir.models.imisModelEnums import ImisHfLevel
from api_fhir.utils import TimeUtils, DbManagerUtils


class LocationConverter(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_hf):
        fhir_location = Location()
        cls.build_fhir_pk(fhir_location, imis_hf.uuid)
        cls.build_fhir_location_identifier(fhir_location, imis_hf)
        cls.build_fhir_location_name(fhir_location, imis_hf)
        cls.build_fhir_location_type(fhir_location, imis_hf)
        cls.build_fhir_location_address(fhir_location, imis_hf)
        cls.build_fhir_location_telecom(fhir_location, imis_hf)
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
    def get_reference_obj_id(cls, imis_hf):
        return imis_hf.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return Location

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        location_uuid = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(HealthFacility, uuid=location_uuid)

    @classmethod
    def createDefaultInsuree(cls, audit_user_id):
        imis_hf = HealthFacility()
        # TODO legalForm isn't covered because that value is missing in the model (value need to be nullable in DB)
        # TODO LocationId isn't covered because that value is missing in the model (value need to be nullable in DB)
        imis_hf.offline = GeneralConfiguration.get_default_value_of_location_offline_attribute()
        imis_hf.care_type = GeneralConfiguration.get_default_value_of_location_care_type()
        imis_hf.validity_from = TimeUtils.now()
        imis_hf.audit_user_id = audit_user_id
        return imis_hf

    @classmethod
    def build_fhir_location_identifier(cls, fhir_location, imis_hf):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_hf)
        cls.build_fhir_hf_code_identifier(identifiers, imis_hf)
        fhir_location.identifier = identifiers

    @classmethod
    def build_fhir_hf_code_identifier(cls, identifiers, imis_hf):
        if imis_hf is not None:
            identifier = cls.build_fhir_identifier(imis_hf.code,
                                                   Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                   Stu3IdentifierConfig.get_fhir_facility_id_type())
            identifiers.append(identifier)

    @classmethod
    def build_imis_hf_identiftier(cls, imis_hf, fhir_location, errors):
        value = cls.get_fhir_identifier_by_code(fhir_location.identifier,
                                                Stu3IdentifierConfig.get_fhir_facility_id_type())
        if value:
            imis_hf.code = value
        cls.valid_condition(imis_hf.code is None, gettext('Missing hf code'), errors)

    @classmethod
    def build_fhir_location_name(cls, fhir_location, imis_hf):
        fhir_location.name = imis_hf.name

    @classmethod
    def build_imis_hf_name(cls, imis_hf, fhir_location, errors):
        name = fhir_location.name
        if not cls.valid_condition(name is None,
                                   gettext('Missing patient `name` attribute'), errors):
            imis_hf.name = name

    @classmethod
    def build_fhir_location_type(cls, fhir_location, imis_hf):
        code = ""
        if imis_hf.level == ImisHfLevel.HEALTH_CENTER.value:
            code = Stu3LocationConfig.get_fhir_code_for_health_center()
        elif imis_hf.level == ImisHfLevel.HOSPITAL.value:
            code = Stu3LocationConfig.get_fhir_code_for_hospital()
        elif imis_hf.level == ImisHfLevel.DISPENSARY.value:
            code = Stu3LocationConfig.get_fhir_code_for_dispensary()

        fhir_location.type = \
            cls.build_codeable_concept(code, Stu3LocationConfig.get_fhir_location_role_type_system())

    @classmethod
    def build_imis_hf_level(cls, imis_hf, fhir_location, errors):
        location_type = fhir_location.type
        if not cls.valid_condition(location_type is None,
                                   gettext('Missing patient `type` attribute'), errors):
            for maritalCoding in location_type.coding:
                if maritalCoding.system == Stu3LocationConfig.get_fhir_location_role_type_system():
                    code = maritalCoding.code
                    if code == Stu3LocationConfig.get_fhir_code_for_health_center():
                        imis_hf.level = ImisHfLevel.HEALTH_CENTER.value
                    elif code == Stu3LocationConfig.get_fhir_code_for_hospital():
                        imis_hf.level = ImisHfLevel.HOSPITAL.value
                    elif code == Stu3LocationConfig.get_fhir_code_for_dispensary():
                        imis_hf.level = ImisHfLevel.DISPENSARY.value

            cls.valid_condition(imis_hf.level is None, gettext('Missing hf level'), errors)

    @classmethod
    def build_fhir_location_address(cls, fhir_location, imis_hf):
        fhir_location.address = cls.build_fhir_address(imis_hf.address, AddressUse.HOME.value,
                                                       AddressType.PHYSICAL.value)

    @classmethod
    def build_imis_hf_address(cls, imis_hf, fhir_location):
        address = fhir_location.address
        if address is not None:
            if address.type == AddressType.PHYSICAL.value:
                imis_hf.address = address.text

    @classmethod
    def build_fhir_location_telecom(cls, fhir_location, imis_hf):
        telecom = []
        if imis_hf.phone is not None:
            phone = LocationConverter.build_fhir_contact_point(imis_hf.phone, ContactPointSystem.PHONE.value,
                                                               ContactPointUse.HOME.value)
            telecom.append(phone)
        if imis_hf.fax is not None:
            fax = LocationConverter.build_fhir_contact_point(imis_hf.fax, ContactPointSystem.FAX.value,
                                                             ContactPointUse.HOME.value)
            telecom.append(fax)
        if imis_hf.email is not None:
            email = LocationConverter.build_fhir_contact_point(imis_hf.email, ContactPointSystem.EMAIL.value,
                                                               ContactPointUse.HOME.value)
            telecom.append(email)
        fhir_location.telecom = telecom

    @classmethod
    def build_imis_hf_contacts(cls, imis_hf, fhir_location):
        telecom = fhir_location.telecom
        if telecom is not None:
            for contact_point in telecom:
                if contact_point.system == ContactPointSystem.PHONE.value:
                    imis_hf.phone = contact_point.value
                elif contact_point.system == ContactPointSystem.FAX.value:
                    imis_hf.fax = contact_point.value
                elif contact_point.system == ContactPointSystem.EMAIL.value:
                    imis_hf.email = contact_point.value
