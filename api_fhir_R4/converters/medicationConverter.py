from medical.models import Item
from api_fhir_R4.converters import R4IdentifierConfig, BaseFHIRConverter, ReferenceConverterMixin
from api_fhir_R4.models import Medication as FHIRMedication, Extension, Money
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
                                              R4IdentifierConfig.get_fhir_uuid_type_code())
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
        fhir_medication.form = imis_medication.package.lstrip()

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


