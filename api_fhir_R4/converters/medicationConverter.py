from medical.models import Item
from api_fhir_R4.converters import R4IdentifierConfig, BaseFHIRConverter, ReferenceConverterMixin
from api_fhir_R4.models import Medication as FHIRMedication, Extension, Money, CodeableConcept, UsageContext, Coding
from django.utils.translation import gettext
from api_fhir_R4.utils import DbManagerUtils
from api_fhir_R4.configurations import GeneralConfiguration
import core


class MedicationConverter(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_medication):
        fhir_medication = FHIRMedication()
        cls.build_fhir_pk(fhir_medication, imis_medication.uuid)
        cls.build_fhir_identifiers(fhir_medication, imis_medication)
        cls.build_fhir_package_form(fhir_medication, imis_medication)
        #cls.build_fhir_package_amount(fhir_medication, imis_medication)
        cls.build_medication_extension(fhir_medication, imis_medication)
        cls.build_fhir_code(fhir_medication, imis_medication)
        cls.build_fhir_frequency_extension(fhir_medication, imis_medication)
        cls.build_fhir_topic_extension(fhir_medication, imis_medication)
        cls.build_fhir_use_context(fhir_medication, imis_medication)
        return fhir_medication

    @classmethod
    def to_imis_obj(cls, fhir_medication, audit_user_id):
        errors = []
        imis_medication = Item()
        cls.build_imis_identifier(imis_medication, fhir_medication, errors)
        cls.build_imis_item_code(imis_medication, fhir_medication, errors)
        cls.build_imis_item_name(imis_medication, fhir_medication, errors)
        cls.build_imis_item_package(imis_medication, fhir_medication, errors)
        cls.check_errors(errors)
        return imis_medication

    @classmethod
    def get_reference_obj_id(cls, imis_medication):
        return imis_medication.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return FHIRMedication

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_medication_code = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(Item, code=imis_medication_code)

    @classmethod
    def build_fhir_identifiers(cls, fhir_medication, imis_medication):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_medication)
        item_code = cls.build_fhir_identifier(imis_medication.code,
                                              R4IdentifierConfig.get_fhir_identifier_type_system(),
                                              R4IdentifierConfig.get_fhir_item_code_type())
        identifiers.append(item_code)
        fhir_medication.identifier = identifiers

    @classmethod
    def build_imis_identifier(cls, imis_medication, fhir_medication, errors):
        value = cls.get_fhir_identifier_by_code(fhir_medication.identifier, R4IdentifierConfig.get_fhir_uuid_type_code())
        if value:
            imis_medication.code = value
        cls.valid_condition(imis_medication.code is None, gettext('Missing the item code'), errors)

    @classmethod
    def build_fhir_package_form(cls, fhir_medication, imis_medication):
        #form = cls.split_package_form(imis_medication.package)
        #fhir_medication.form = form
        fhir_medication.form = cls.build_codeable_concept("package", text=imis_medication.package.lstrip())

    """
    @classmethod
    def split_package_form(cls, form):
        form = form.lstrip()
        if " " not in form:
            return form
        if " " in form:
            form = form.split(' ', 1)
            form = form[1]
            return form

    @classmethod
    def build_fhir_package_amount(cls, fhir_medication, imis_medication):
        amount = cls.split_package_amount(imis_medication.package)
        fhir_medication.amount = amount

    @classmethod
    def split_package_amount(cls, amount):
        amount = amount.lstrip()
        if " " not in amount:
            return None
        if " " in amount:
            amount = amount.split(' ', 1)
            amount = amount[0]
            return int(amount)
    """

    @classmethod
    def build_medication_extension(cls, fhir_medication, imis_medication):
        cls.build_unit_price(fhir_medication, imis_medication)
        return fhir_medication

    @classmethod
    def build_unit_price(cls, fhir_medication, imis_medication):
        unit_price = cls.build_unit_price_extension(imis_medication.price)
        fhir_medication.extension.append(unit_price)

    @classmethod
    def build_unit_price_extension(cls, value):
        extension = Extension()
        money = Money()
        extension.url = "unitPrice"
        extension.valueMoney = money
        extension.valueMoney.value = value
        extension.valueMoney.currency = core.currency
        return extension

    @classmethod
    def build_fhir_code(cls, fhir_medication, imis_medication):
        fhir_medication.code = cls.build_codeable_concept(imis_medication.code, text=imis_medication.name)

    @classmethod
    def build_imis_item_code(cls, imis_medication, fhir_medication, errors):
        item_code = fhir_medication.code.coding
        if not cls.valid_condition(item_code is None,
                                   gettext('Missing medication `item_code` attribute'), errors):
            imis_medication.code = item_code

    @classmethod
    def build_imis_item_name(cls, imis_medication, fhir_medication, errors):
        item_name = fhir_medication.code.text
        if not cls.valid_condition(item_name is None,
                                   gettext('Missing medication `item_name` attribute'), errors):
            imis_medication.name = item_name

    @classmethod
    def build_imis_item_package(cls, imis_medication, fhir_medication, errors):
        form = fhir_medication.form
        amount = fhir_medication.amount
        package = [amount, form]
        if not cls.valid_condition(package is None,
                                   gettext('Missing medication `form` and `amount` attribute'), errors):
            imis_medication.package = package

    @classmethod
    def build_fhir_frequency_extension(cls, fhir_medication, imis_medication):
        serv_price = cls.build_fhir_item_frequency_extension(imis_medication)
        fhir_medication.extension.append(serv_price)

    @classmethod
    def build_fhir_item_frequency_extension(cls, imis_medication):
        extension = Extension()
        extension.url = "frequency"
        extension.valueInteger = imis_medication.frequency
        return extension

    @classmethod
    def build_fhir_topic_extension(cls, fhir_medication, imis_medication):
        item_type = cls.build_fhir_item_type_extension(imis_medication)
        fhir_medication.extension.append(item_type)

    @classmethod
    def build_fhir_item_type_extension(cls, imis_medication):
        extension = Extension()
        extension.url = "topic"
        extension.valueCodeableConcept = cls.build_codeable_concept("DefinitionTopic",
                                                                    "http://terminology.hl7.org/CodeSystem/definition-topic",
                                                                    text=imis_medication.type)
        return extension

    @classmethod
    def build_fhir_use_context(cls, fhir_medication, imis_medication):
        gender = cls.build_fhir_gender(imis_medication)
        fhir_medication.extension.append(gender)
        age = cls.build_fhir_age(imis_medication)
        fhir_medication.extension.append(age)
        venue = cls.build_fhir_venue(imis_medication)
        fhir_medication.extension.append(venue)

    @classmethod
    def build_fhir_gender(cls, imis_medication):
        male = cls.build_fhir_male(imis_medication)
        female = cls.build_fhir_female(imis_medication)
        if male == "":
            male = None
        if female == "":
            female = None
        extension = Extension()
        extension.url = "useContextGender"
        extension.valueUsageContext = UsageContext()
        extension.valueUsageContext.code = Coding()
        extension.valueUsageContext.code.code = "gender"
        extension.valueUsageContext.valueCodeableConcept = CodeableConcept()
        if male is not None:
            coding_male = Coding()
            coding_male.code = male
            coding_male.display = "Male"
            extension.valueUsageContext.valueCodeableConcept.coding.append(coding_male)
        if female is not None:
            coding_female = Coding()
            coding_female.code = female
            coding_female.display = "Female"
            extension.valueUsageContext.valueCodeableConcept.coding.append(coding_female)
            extension.valueUsageContext.valueCodeableConcept.text = "Male or Female"
        return extension

    @classmethod
    def build_fhir_age(cls, imis_medication):
        adult = cls.build_fhir_adult(imis_medication)
        kid = cls.build_fhir_kid(imis_medication)
        if adult == "":
            adult = None
        if kid == "":
            kid = None
        extension = Extension()
        extension.url = "useContextAge"
        extension.valueUsageContext = UsageContext()
        extension.valueUsageContext.code = Coding()
        extension.valueUsageContext.code.code = "age"
        extension.valueUsageContext.valueCodeableConcept = CodeableConcept()
        if adult is not None:
            coding_adult = Coding()
            coding_adult.code = adult
            coding_adult.display = "Adult"
            extension.valueUsageContext.valueCodeableConcept.coding.append(coding_adult)
        if kid is not None:
            coding_kid = Coding()
            coding_kid.code = kid
            coding_kid.display = "Kid"
            extension.valueUsageContext.valueCodeableConcept.coding.append(coding_kid)
            extension.valueUsageContext.valueCodeableConcept.text = "Adult or Kid"
        return extension

    @classmethod
    def build_fhir_venue(cls, imis_medication):
        display = ""
        if imis_medication.care_type == "O":
            display = "Out-patient"
        if imis_medication.care_type == "I":
            display = "In-patient"
        if imis_medication.care_type == "B":
            display = "Both"

        extension = Extension()
        if imis_medication.care_type is not None:
            extension.url = "useContextVenue"
            extension.valueUsageContext = UsageContext()
            extension.valueUsageContext.code = Coding()
            extension.valueUsageContext.code.code = "venue"
            extension.valueUsageContext.valueCodeableConcept = CodeableConcept()
            coding_venue = Coding()
            coding_venue.code = imis_medication.care_type
            coding_venue.display = display
            extension.valueUsageContext.valueCodeableConcept.coding.append(coding_venue)
            extension.valueUsageContext.valueCodeableConcept.text = "Clinical Venue"
        return extension

    @classmethod
    def build_fhir_male(cls, imis_medication):
        item_pat_cat = imis_medication.patient_category
        male = ""
        if item_pat_cat > 8:
            kid = "K"
            item_pat_cat = item_pat_cat - 8
        if item_pat_cat > 4:
            adult = "A"
            item_pat_cat = item_pat_cat - 4
        if item_pat_cat > 2:
            female = "F"
            item_pat_cat = item_pat_cat - 2
        if item_pat_cat == 1:
            male = "M"
        return male

    @classmethod
    def build_fhir_female(cls, imis_medication):
        item_pat_cat = imis_medication.patient_category
        female = ""
        if item_pat_cat > 8:
            kid = "K"
            item_pat_cat = item_pat_cat - 8
        if item_pat_cat > 4:
            adult = "A"
            item_pat_cat = item_pat_cat - 4
        if item_pat_cat >= 2:
            female = "F"
        return female

    @classmethod
    def build_fhir_adult(cls, imis_medication):
        item_pat_cat = imis_medication.patient_category
        adult = ""
        if item_pat_cat > 8:
            kid = "K"
            item_pat_cat = item_pat_cat - 8
        if item_pat_cat >= 4:
            adult = "A"
        return adult

    @classmethod
    def build_fhir_kid(cls, imis_medication):
        item_pat_cat = imis_medication.patient_category
        kid = ""
        if item_pat_cat >= 8:
            kid = "K"
        return kid

    @classmethod
    def build_imis_item_pat_cat(cls, imis_medication, fhir_medication):
        item_pat_cat = fhir_medication.useContext.code
        number = 0
        if "K" in item_pat_cat:
            number = number + 8
        if "A" in item_pat_cat:
            number = number + 4
        if "F" in item_pat_cat:
            number = number + 2
        if "M" in item_pat_cat:
            number = number + 1

        imis_medication.patient_category = number

    @classmethod
    def build_imis_serv_care_type(cls, imis_medication, fhir_medication, errors):
        serv_care_type = fhir_medication.useContext.text
        if not cls.valid_condition(serv_care_type is None,
                                   gettext('Missing activity definition `serv care type` attribute'), errors):
            imis_medication.care_type = serv_care_type

