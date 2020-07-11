from django.utils.translation import gettext
from insuree.models import Insuree, Gender, Education, Profession, Family
from location.models import Location

from api_fhir_R4.configurations import R4IdentifierConfig, GeneralConfiguration, R4MaritalConfig
from api_fhir_R4.converters import BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin
from api_fhir_R4.converters.healthcareServiceConverter import HealthcareServiceConverter
from api_fhir_R4.models import Patient, AdministrativeGender, ImisMaritalStatus, Extension, PatientLink, Attachment
from api_fhir_R4.models.address import AddressUse, AddressType
from api_fhir_R4.utils import TimeUtils, DbManagerUtils

class PatientConverter(BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_insuree):
        fhir_patient = Patient()
        cls.build_fhir_pk(fhir_patient, imis_insuree.uuid)
        cls.build_human_names(fhir_patient, imis_insuree)
        cls.build_fhir_identifiers(fhir_patient, imis_insuree)
        cls.build_fhir_birth_date(fhir_patient, imis_insuree)
        cls.build_fhir_gender(fhir_patient, imis_insuree)
        cls.build_fhir_marital_status(fhir_patient, imis_insuree)
        cls.build_fhir_telecom(fhir_patient, imis_insuree)
        cls.build_fhir_addresses(fhir_patient, imis_insuree)
        cls.build_fhir_extentions(fhir_patient, imis_insuree)
        cls.build_poverty_status(fhir_patient, imis_insuree)
        cls.build_fhir_related_person(fhir_patient, imis_insuree)
        cls.build_fhir_photo(fhir_patient, imis_insuree)
        cls.build_fhir_general_practitioner(fhir_patient, imis_insuree)
        return fhir_patient

    @classmethod
    def to_imis_obj(cls, fhir_patient, audit_user_id):
        errors = []
        imis_insuree = cls.createDefaultInsuree(audit_user_id)
        # TODO the familyid isn't covered because that value is missing in the model
        # TODO the photoId isn't covered because that value is missing in the model
        # TODO the typeofid isn't covered because that value is missing in the model
        cls.build_imis_names(imis_insuree, fhir_patient, errors)
        cls.build_imis_identifiers(imis_insuree, fhir_patient)
        cls.build_imis_birth_date(imis_insuree, fhir_patient, errors)
        cls.build_imis_gender(imis_insuree, fhir_patient)
        cls.build_imis_marital(imis_insuree, fhir_patient)
        cls.build_imis_contacts(imis_insuree, fhir_patient)
        cls.build_imis_addresses(imis_insuree, fhir_patient)
        cls.build_imis_related_person(imis_insuree, errors)
        cls.build_imis_photo(imis_insuree, fhir_patient, errors)
        cls.check_errors(errors)
        return imis_insuree

    @classmethod
    def get_reference_obj_id(cls, imis_insuree):
        return imis_insuree.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return Patient

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_insuree_uuid = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(Insuree, uuid=imis_insuree_uuid)

    @classmethod
    def createDefaultInsuree(cls, audit_user_id):
        imis_insuree = Insuree()
        imis_insuree.head = GeneralConfiguration.get_default_value_of_patient_head_attribute()
        imis_insuree.card_issued = GeneralConfiguration.get_default_value_of_patient_card_issued_attribute()
        imis_insuree.validity_from = TimeUtils.now()
        imis_insuree.audit_user_id = audit_user_id
        return imis_insuree

    @classmethod
    def build_human_names(cls, fhir_patient, imis_insuree):
        name = cls.build_fhir_names_for_person(imis_insuree)
        fhir_patient.name = [name]

    @classmethod
    def build_imis_names(cls, imis_insuree, fhir_patient, errors):
        names = fhir_patient.name
        if not cls.valid_condition(names is None, gettext('Missing patient `name` attribute'), errors):
            imis_insuree.last_name, imis_insuree.other_names = cls.build_imis_last_and_other_name(names)
            cls.valid_condition(imis_insuree.last_name is None, gettext('Missing patient family name'), errors)
            cls.valid_condition(imis_insuree.other_names is None, gettext('Missing patient given name'), errors)

    @classmethod
    def build_fhir_identifiers(cls, fhir_patient, imis_insuree):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_insuree)
        cls.build_fhir_chfid_identifier(identifiers, imis_insuree)
        cls.build_fhir_passport_identifier(identifiers, imis_insuree)
        fhir_patient.identifier = identifiers

    @classmethod
    def build_imis_identifiers(cls, imis_insuree, fhir_patient):
        value = cls.get_fhir_identifier_by_code(fhir_patient.identifier,
                                                R4IdentifierConfig.get_fhir_chfid_type_code())
        if value:
            imis_insuree.chf_id = value
        value = cls.get_fhir_identifier_by_code(fhir_patient.identifier,
                                                R4IdentifierConfig.get_fhir_passport_type_code())
        if value:
            imis_insuree.passport = value

    @classmethod
    def build_fhir_chfid_identifier(cls, identifiers, imis_insuree):
        if imis_insuree.chf_id is not None:
            identifier = cls.build_fhir_identifier(imis_insuree.chf_id,
                                                   R4IdentifierConfig.get_fhir_identifier_type_system(),
                                                   R4IdentifierConfig.get_fhir_chfid_type_code())
            identifiers.append(identifier)

    @classmethod
    def build_fhir_passport_identifier(cls, identifiers, imis_insuree):
        if hasattr(imis_insuree, "typeofid") and imis_insuree.typeofid is not None:
            pass  # TODO typeofid isn't provided, this section should contain logic used to create passport field based on typeofid
        elif imis_insuree.passport is not None:
            identifier = cls.build_fhir_identifier(imis_insuree.passport,
                                                   R4IdentifierConfig.get_fhir_identifier_type_system(),
                                                   R4IdentifierConfig.get_fhir_passport_type_code())
            identifiers.append(identifier)

    @classmethod
    def build_fhir_birth_date(cls, fhir_patient, imis_insuree):
        fhir_patient.birthDate = imis_insuree.dob.isoformat()

    @classmethod
    def build_imis_birth_date(cls, imis_insuree, fhir_patient, errors):
        birth_date = fhir_patient.birthDate
        if not cls.valid_condition(birth_date is None, gettext('Missing patient `birthDate` attribute'), errors):
            imis_insuree.dob = TimeUtils.str_to_date(birth_date)

    @classmethod
    def build_fhir_gender(cls, fhir_patient, imis_insuree):
        if hasattr(imis_insuree, "gender") and imis_insuree.gender is not None:
            code = imis_insuree.gender.code
            if code == GeneralConfiguration.get_male_gender_code():
                fhir_patient.gender = AdministrativeGender.MALE.value
            elif code == GeneralConfiguration.get_female_gender_code():
                fhir_patient.gender = AdministrativeGender.FEMALE.value
            elif code == GeneralConfiguration.get_other_gender_code():
                fhir_patient.gender = AdministrativeGender.OTHER.value
        else:
            fhir_patient.gender = AdministrativeGender.UNKNOWN.value

    @classmethod
    def build_imis_gender(cls, imis_insuree, fhir_patient):
        gender = fhir_patient.gender
        if gender is not None:
            imis_gender_code = None
            if gender == AdministrativeGender.MALE.value:
                imis_gender_code = GeneralConfiguration.get_male_gender_code()
            elif gender == AdministrativeGender.FEMALE.value:
                imis_gender_code = GeneralConfiguration.get_female_gender_code()
            elif gender == AdministrativeGender.OTHER.value:
                imis_gender_code = GeneralConfiguration.get_other_gender_code()
            if imis_gender_code is not None:
                imis_insuree.gender = Gender.objects.get(pk=imis_gender_code)

    @classmethod
    def build_fhir_marital_status(cls, fhir_patient, imis_insuree):
        if imis_insuree.marital is not None:
            if imis_insuree.marital == ImisMaritalStatus.MARRIED.value:
                fhir_patient.maritalStatus = \
                    cls.build_codeable_concept(R4MaritalConfig.get_fhir_married_code(),
                                               R4MaritalConfig.get_fhir_marital_status_system())
            elif imis_insuree.marital == ImisMaritalStatus.SINGLE.value:
                fhir_patient.maritalStatus = \
                    cls.build_codeable_concept(R4MaritalConfig.get_fhir_never_married_code(),
                                               R4MaritalConfig.get_fhir_marital_status_system())
            elif imis_insuree.marital == ImisMaritalStatus.DIVORCED.value:
                fhir_patient.maritalStatus = \
                    cls.build_codeable_concept(R4MaritalConfig.get_fhir_divorced_code(),
                                               R4MaritalConfig.get_fhir_marital_status_system())
            elif imis_insuree.marital == ImisMaritalStatus.WIDOWED.value:
                fhir_patient.maritalStatus = \
                    cls.build_codeable_concept(R4MaritalConfig.get_fhir_widowed_code(),
                                               R4MaritalConfig.get_fhir_marital_status_system())
            elif imis_insuree.marital == ImisMaritalStatus.NOT_SPECIFIED.value:
                fhir_patient.maritalStatus = \
                    cls.build_codeable_concept(R4MaritalConfig.get_fhir_unknown_marital_status_code(),
                                               R4MaritalConfig.get_fhir_marital_status_system())

    @classmethod
    def build_imis_marital(cls, imis_insuree, fhir_patient):
        marital_status = fhir_patient.maritalStatus
        if marital_status is not None:
            for maritialCoding in marital_status.coding:
                if maritialCoding.system == R4MaritalConfig.get_fhir_marital_status_system():
                    code = maritialCoding.code
                    if code == R4MaritalConfig.get_fhir_married_code():
                        imis_insuree.marital = ImisMaritalStatus.MARRIED.value
                    elif code == R4MaritalConfig.get_fhir_never_married_code():
                        imis_insuree.marital = ImisMaritalStatus.SINGLE.value
                    elif code == R4MaritalConfig.get_fhir_divorced_code():
                        imis_insuree.marital = ImisMaritalStatus.DIVORCED.value
                    elif code == R4MaritalConfig.get_fhir_widowed_code():
                        imis_insuree.marital = ImisMaritalStatus.WIDOWED.value
                    elif code == R4MaritalConfig.get_fhir_unknown_marital_status_code():
                        imis_insuree.marital = ImisMaritalStatus.NOT_SPECIFIED.value

    @classmethod
    def build_fhir_telecom(cls, fhir_patient, imis_insuree):
        fhir_patient.telecom = cls.build_fhir_telecom_for_person(phone=imis_insuree.phone, email=imis_insuree.email)

    @classmethod
    def build_imis_contacts(cls, imis_insuree, fhir_patient):
        imis_insuree.phone, imis_insuree.email = cls.build_imis_phone_num_and_email(fhir_patient.telecom)

    @classmethod
    def build_fhir_addresses(cls, fhir_patient, imis_insuree):
        addresses = []
        if imis_insuree.current_address is not None:
            current_address = cls.build_fhir_address(imis_insuree.current_address, AddressUse.HOME.value,
                                                     AddressType.PHYSICAL.value)
            addresses.append(current_address)
        if imis_insuree.geolocation is not None:
            geolocation = cls.build_fhir_address(imis_insuree.geolocation, AddressUse.HOME.value,
                                                 AddressType.BOTH.value)
            addresses.append(geolocation)
        fhir_patient.address = addresses

    @classmethod
    def build_imis_addresses(cls, imis_insuree, fhir_patient):
        addresses = fhir_patient.address
        if addresses is not None:
            for address in addresses:
                if address.type == AddressType.PHYSICAL.value:
                    imis_insuree.current_address = address.text
                elif address.type == AddressType.BOTH.value:
                    imis_insuree.geolocation = address.text

    @classmethod
    def build_fhir_extentions(cls, fhir_patient, imis_insuree):
        fhir_patient.extension = []

        def build_extension(fhir_patient, imis_insuree,value):
            extension = Extension()
            if value == "head":
                extension.url = "https://openimis.atlassian.net/wiki/spaces/OP/pages/960069653/FHIR+extension+isHead"
                extension.valueBoolean = imis_insuree.head
            elif value == "validity_from":
                extension.url = "https://openimis.atlassian.net/wiki/spaces/OP/pages/960331779/FHIR+extension+registrationDate"
                if imis_insuree.validity_from is None:
                    extension.valueString = ""
                else :
                    extension.valueString = imis_insuree.validity_from
            elif value == "family.location.code":
                extension.url = "https://openimis.atlassian.net/wiki/spaces/OP/pages/960495619/FHIR+extension+Location"
                if hasattr(imis_insuree, "family") and imis_insuree.family is not None:
                    if imis_insuree.family.location.code is not None:
                        extension.valueString = imis_insuree.family.location.code
                    else :
                        extension.valueString = ""
                else:
                     extension.valueString = ""

            elif value == "education.education":
                extension.url = "https://openimis.atlassian.net/wiki/spaces/OP/pages/960331788/FHIR+extension+Education"
                if hasattr(imis_insuree, "education") and imis_insuree.education is not None:
                    if imis_insuree.education.education is not None:
                        extension.valueString = imis_insuree.education.education
                    else :
                        extension.valueString = ""
                else:
                     extension.valueString = ""
            else :
                extension.url = "https://openimis.atlassian.net/wiki/spaces/OP/pages/960135203/FHIE+extension+Profession"
                if hasattr(imis_insuree, "profession") and imis_insuree.profession is not None:
                    if imis_insuree.profession.profession is not None:
                        extension.valueString = imis_insuree.profession.profession
                    else :
                        extension.valueString = ""
                else:
                     extension.valueString = ""

            fhir_patient.extension.append(extension)
        build_extension(fhir_patient, imis_insuree, "head")
        build_extension(fhir_patient, imis_insuree, "validity_from")
        build_extension(fhir_patient, imis_insuree, "family.location.code")
        build_extension(fhir_patient, imis_insuree, "education.education")
        build_extension(fhir_patient, imis_insuree, "profession.profession")

    @classmethod
    def build_poverty_status(cls, fhir_patient, imis_insuree):
        poverty_status = cls.build_poverty_status_extension(imis_insuree)
        if poverty_status.valueBoolean is not None:
            fhir_patient.extension.append(poverty_status)

    @classmethod
    def build_poverty_status_extension(cls, imis_insuree):
        extension = Extension()
        extension.url = "povertyStatus"
        extension.valueBoolean = imis_insuree.family.poverty
        return extension

    @classmethod
    def build_fhir_related_person(cls, fhir_patient, imis_insuree):
        fhir_link = PatientLink()
        if imis_insuree.relationship is not None:
            fhir_link.other = PatientConverter.build_fhir_resource_reference(imis_insuree.family.head_insuree)
            fhir_link.type = imis_insuree.relationship.relation
            fhir_patient.link = [fhir_link]

    @classmethod
    def build_imis_related_person(cls, imis_insuree, errors):
        fhir_link = PatientLink()
        relation = fhir_link.type
        head = fhir_link.other
        if not cls.valid_condition(head is None, gettext('Missing patient `head` attribute'), errors):
            imis_insuree.family.head_insuree = head
        if not cls.valid_condition(relation is None, gettext('Missing patient `relation` attribute'), errors):
            imis_insuree.relationship.relation = relation

    @classmethod
    def build_fhir_photo(cls, fhir_patient, imis_insuree):
        photo = Attachment()
        if imis_insuree.photo is not None:
            photo.creation = imis_insuree.photo.date.isoformat()
            url = imis_insuree.photo.folder + imis_insuree.photo.filename
            photo.url = url
            fhir_patient.photo = [photo]

    @classmethod
    def build_imis_photo(cls, imis_insuree, fhir_patient, errors):
        url = fhir_patient.photo.url
        url = url.split("\\", 2)
        folder = url[0]
        filename = url[1]
        creation = fhir_patient.photo.creation
        if not cls.valid_condition(creation is None, gettext('Missing patient `photo url` attribute'), errors):
            imis_insuree.photo.date = TimeUtils.str_to_date(creation)
        if not cls.valid_condition(folder is None, gettext('Missing patient `photo folder` attribute'), errors):
            imis_insuree.photo.folder = folder
        if not cls.valid_condition(filename is None, gettext('Missing patient `photo filename` attribute'), errors):
            imis_insuree.photo.filename = filename

    @classmethod
    def build_fhir_general_practitioner(cls, fhir_patient, imis_insuree):
        if imis_insuree.health_facility is not None:
            fhir_patient.generalPractitioner = [HealthcareServiceConverter.\
                build_fhir_resource_reference(imis_insuree.health_facility)]




