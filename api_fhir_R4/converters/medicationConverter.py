from medical.models import Item
from api_fhir_R4.converters import R4IdentifierConfig, BaseFHIRConverter
from api_fhir_R4.models import Medication as FHIRMedication, Money
from django.utils.translation import gettext

class MedicationConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_medication):
        fhir_medication = FHIRMedication()
        cls.build_fhir_pk(fhir_medication, imis_medication.uuid)
        cls.build_fhir_identifiers(fhir_medication, imis_medication)
        cls.build_fhir_package_form(fhir_medication, imis_medication)
        cls.build_fhir_package_amount(fhir_medication, imis_medication)
        cls.build_fhir_unitPrice(fhir_medication, imis_medication)

    @classmethod
    def to_imis_obj(cls, fhir_medication, audit_user_id):
        errors = []
        imis_medication = Item()
        cls.build_imis_identifier(imis_medication, fhir_medication, errors)
        cls.check_errors(errors)
        return imis_medication

    @classmethod
    def get_reference_obj_id(cls, imis_medication):
        return imis_medication.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return FHIRMedication

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
    def build_fhir_package_form(cls, fhir_medication, imis_mediaction):
        form = cls.split_package_form(imis_mediaction.package)
        fhir_medication.form = form

    @classmethod
    def split_package_form(cls, form):
        form = form.split(' ')
        form = form[1]
        return form

    @classmethod
    def build_fhir_package_amount(cls, fhir_medication, imis_medicaton):
        amount = cls.split_package_amount(imis_medicaton.package)
        fhir_medication.amount = amount

    @classmethod
    def split_package_amount(cls, amount):
        amount = amount.split(' ')
        amount = int(amount[0])
        return amount

    @classmethod
    def build_fhir_unitPrice(cls, fhir_medication, imis_medication):
        


