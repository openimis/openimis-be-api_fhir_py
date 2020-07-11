from medical.models import Service
from api_fhir_R4.models import ActivityDefinition, Extension, Money, UsageContext, CodeableConcept, Coding
from api_fhir_R4.converters import R4IdentifierConfig, BaseFHIRConverter, ReferenceConverterMixin
from django.utils.translation import gettext
from api_fhir_R4.utils import DbManagerUtils, TimeUtils
import core


class ActivityDefinitionConverter(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_activity_definition):
        fhir_activity_definition = ActivityDefinition()
        cls.build_fhir_pk(fhir_activity_definition, imis_activity_definition.uuid)
        cls.build_fhir_identifiers(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_status(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_date(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_name(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_title(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_use_context(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_topic(fhir_activity_definition, imis_activity_definition)
        cls.build_activity_definition_extension(fhir_activity_definition, imis_activity_definition)
        cls.build_fhir_frequency_extension(fhir_activity_definition, imis_activity_definition)
        return fhir_activity_definition

    @classmethod
    def to_imis_obj(cls, fhir_activity_definition, audit_user_id):
        errors = []
        imis_activity_definition = Service()
        cls.build_imis_identifier(imis_activity_definition, fhir_activity_definition, errors)
        cls.build_imis_validity_from(imis_activity_definition, fhir_activity_definition, errors)
        cls.build_imis_serv_code(imis_activity_definition, fhir_activity_definition, errors)
        cls.build_imis_serv_name(imis_activity_definition, fhir_activity_definition, errors)
        cls.build_imis_serv_type(imis_activity_definition, fhir_activity_definition, errors)
        cls.build_imis_serv_pat_cat(imis_activity_definition, fhir_activity_definition)
        cls.build_imis_serv_category(imis_activity_definition, fhir_activity_definition, errors)
        cls.build_imis_serv_care_type(imis_activity_definition, fhir_activity_definition, errors)
        cls.check_errors(errors)
        return imis_activity_definition

    @classmethod
    def get_reference_obj_id(cls, imis_activity_definition):
        return imis_activity_definition.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return ActivityDefinition

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_activity_definition_code = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(Service, code=imis_activity_definition_code)

    @classmethod
    def build_fhir_identifiers(cls, fhir_activity_definition, imis_activity_definition):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_activity_definition)
        serv_code = cls.build_fhir_identifier(imis_activity_definition.code,
                                              R4IdentifierConfig.get_fhir_identifier_type_system(),
                                              R4IdentifierConfig.get_fhir_service_code_type())
        identifiers.append(serv_code)
        fhir_activity_definition.identifier = identifiers

    @classmethod
    def build_imis_identifier(cls, imis_activity_definition, fhir_activity_definition, errors):
        value = cls.get_fhir_identifier_by_code(fhir_activity_definition.identifier,
                                                R4IdentifierConfig.get_fhir_uuid_type_code())
        if value:
            imis_activity_definition.code = value
        cls.valid_condition(imis_activity_definition.code is None, gettext('Missing the service code'), errors)

    @classmethod
    def build_fhir_status(cls, fhir_activity_definition, imis_activity_definition):
        fhir_activity_definition.status = "active"

    @classmethod
    def build_fhir_date(cls, fhir_activity_definition, imis_activity_definition):
        fhir_activity_definition.date = imis_activity_definition.validity_from.isoformat()

    @classmethod
    def build_imis_validity_from(cls, imis_activity_definition, fhir_activity_definition, errors):
        validity_from = fhir_activity_definition.date
        if not cls.valid_condition(validity_from is None,
                                   gettext('Missing activity definition `validity from` attribute'), errors):
            imis_activity_definition.validity_from = TimeUtils.str_to_date(validity_from)

    @classmethod
    def build_fhir_name(cls, fhir_activity_definition, imis_activity_definition):
        fhir_activity_definition.name = imis_activity_definition.code

    @classmethod
    def build_imis_serv_code(cls, imis_activity_definition, fhir_activity_definition, errors):
        serv_code = fhir_activity_definition.name
        if not cls.valid_condition(serv_code is None,
                                   gettext('Missing activity definition `serv code` attribute'), errors):
            imis_activity_definition.code = serv_code

    @classmethod
    def build_fhir_title(cls, fhir_activity_definition, imis_activity_definition):
        fhir_activity_definition.title = imis_activity_definition.name

    @classmethod
    def build_imis_serv_name(cls, imis_activity_definition, fhir_activity_definition, errors):
        serv_name = fhir_activity_definition.title
        if not cls.valid_condition(serv_name is None,
                                   gettext('Missing activity definition `serv name` attribute'), errors):
            imis_activity_definition.name = serv_name
    """
    @classmethod
    def build_fhir_use_context(cls, fhir_activity_definition, imis_activity_definition):
        use_context = cls.build_fhir_use_context_codes(imis_activity_definition)
        for i in use_context:
            if i is not None:
                fhir_activity_definition.useContext.append(i)

    @classmethod
    def build_fhir_use_context_codes(cls, imis_activity_definition):

        male = cls.build_fhir_male(imis_activity_definition)
        female = cls.build_fhir_female(imis_activity_definition)
        adult = cls.build_fhir_adult(imis_activity_definition)
        kid = cls.build_fhir_kid(imis_activity_definition)
        workflow = cls.build_fhir_workflow(imis_activity_definition)
        venue = cls.build_fhir_venue(imis_activity_definition)

        if male.valueCodeableConcept.text == "":
            male = None
        if female.valueCodeableConcept.text == "":
            female = None
        if adult.valueCodeableConcept.text == "":
            adult = None
        if kid.valueCodeableConcept.text == "":
            kid = None
        if workflow.valueCodeableConcept.text == "":
            workflow = None
        if venue.valueCodeableConcept.text == "":
            venue = None

        use_context = [male, female, adult, kid, workflow, venue]

        return use_context

    @classmethod
    def build_fhir_male(cls, imis_activity_definition):
        extension = Extension()
        serv_pat_cat = imis_activity_definition.patient_category
        male = ""
        if serv_pat_cat > 8:
            kid = "K"
            serv_pat_cat = serv_pat_cat - 8
        if serv_pat_cat > 4:
            adult = "A"
            serv_pat_cat = serv_pat_cat - 4
        if serv_pat_cat > 2:
            female = "F"
            serv_pat_cat = serv_pat_cat - 2
        if serv_pat_cat == 1:
            male = "M"

        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.text = male
        extension.valueCodeableConcept.coding = ["gender"]
        return extension

    @classmethod
    def build_fhir_female(cls, imis_activity_definition):
        extension = Extension()
        serv_pat_cat = imis_activity_definition.patient_category
        female = ""
        if serv_pat_cat > 8:
            kid = "K"
            serv_pat_cat = serv_pat_cat - 8
        if serv_pat_cat > 4:
            adult = "A"
            serv_pat_cat = serv_pat_cat - 4
        if serv_pat_cat >= 2:
            female = "F"

        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.text = female
        extension.valueCodeableConcept.coding = ["gender"]
        return extension

    @classmethod
    def build_fhir_adult(cls, imis_activity_definition):
        extension = Extension()
        serv_pat_cat = imis_activity_definition.patient_category
        adult = ""
        if serv_pat_cat > 8:
            kid = "K"
            serv_pat_cat = serv_pat_cat - 8
        if serv_pat_cat >= 4:
            adult = "A"

        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.text = adult
        extension.valueCodeableConcept.coding = ["age"]
        return extension

    @classmethod
    def build_fhir_kid(cls, imis_activity_definition):
        extension = Extension()
        serv_pat_cat = imis_activity_definition.patient_category
        kid = ""
        if serv_pat_cat >= 8:
            kid = "K"

        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.text = kid
        extension.valueCodeableConcept.coding = ["age"]
        return extension

    @classmethod
    def build_fhir_workflow(cls, imis_activity_definition):
        extension = Extension()
        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.text = imis_activity_definition.category
        extension.valueCodeableConcept.coding = ["workflow"]
        return extension

    @classmethod
    def build_fhir_venue(cls, imis_activity_definition):
        extension = Extension()
        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.text = imis_activity_definition.care_type
        extension.valueCodeableConcept.coding = ["venue"]
        return extension
    """
    @classmethod
    def build_imis_serv_pat_cat(cls, imis_activity_definition, fhir_activity_definition):
        serv_pat_cat = fhir_activity_definition.useContext.code
        number = 0
        if "K" in serv_pat_cat:
            number = number + 8
        if "A" in serv_pat_cat:
            number = number + 4
        if "F" in serv_pat_cat:
            number = number + 2
        if "M" in serv_pat_cat:
            number = number + 1

        imis_activity_definition.patient_category = number

    @classmethod
    def build_imis_serv_category(cls, imis_activity_definition, fhir_activity_definition, errors):
        serv_category = fhir_activity_definition.useContext.text
        if not cls.valid_condition(serv_category is None,
                                   gettext('Missing activity definition `serv category` attribute'), errors):
            imis_activity_definition.category = serv_category

    @classmethod
    def build_imis_serv_care_type(cls, imis_activity_definition, fhir_activity_definition, errors):
        serv_care_type = fhir_activity_definition.useContext.text
        if not cls.valid_condition(serv_care_type is None,
                                   gettext('Missing activity definition `serv care type` attribute'), errors):
            imis_activity_definition.care_type = serv_care_type

    @classmethod
    def build_fhir_topic(cls, fhir_activity_definition, imis_activity_definition):
        fhir_activity_definition.topic = [cls.build_codeable_concept(
            "DefinitionTopic", "http://terminology.hl7.org/CodeSystem/definition-topic",
            text=imis_activity_definition.type)]

    @classmethod
    def build_imis_serv_type(cls, imis_activity_definition, fhir_activity_definition, errors):
        serv_type = fhir_activity_definition.topic
        if not cls.valid_condition(serv_type is None,
                                   gettext('Missing activity definition `serv type` attribute'), errors):
            imis_activity_definition.topic = serv_type

    @classmethod
    def build_fhir_code(cls, fhir_activity_definition, imis_activity_definition):
        fhir_activity_definition.code = cls.build_codeable_concept(imis_activity_definition.code,
                                                                   text=imis_activity_definition.name)

    @classmethod
    def build_activity_definition_extension(cls, fhir_activity_definition, imis_activity_definition):
        cls.build_unit_price(fhir_activity_definition, imis_activity_definition)
        return fhir_activity_definition

    @classmethod
    def build_unit_price(cls, fhir_activity_definition, imis_activity_definition):
        unit_price = cls.build_unit_price_extension(imis_activity_definition.price)
        fhir_activity_definition.extension.append(unit_price)

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
    def build_fhir_frequency_extension(cls, fhir_activity_definition, imis_activity_definition):
        serv_price = cls.build_fhir_serv_frequency_extension(imis_activity_definition)
        fhir_activity_definition.extension.append(serv_price)

    @classmethod
    def build_fhir_serv_frequency_extension(cls, imis_activity_definition):
        extension = Extension()
        extension.url = "frequency"
        extension.valueInteger = imis_activity_definition.frequency
        return extension

    @classmethod
    def build_fhir_use_context(cls, fhir_activity_definition, imis_activity_definition):
        use_context = cls.build_fhir_use_context_context(imis_activity_definition)
        fhir_activity_definition.useContext = use_context

    @classmethod
    def build_fhir_use_context_context(cls, imis_activity_definition):
        gender = cls.build_fhir_gender(imis_activity_definition)
        age = cls.build_fhir_age(imis_activity_definition)
        workflow = cls.build_fhir_workflow(imis_activity_definition)
        venue = cls.build_fhir_venue(imis_activity_definition)

        usage_context_gender = UsageContext()
        usage_context_age = UsageContext()
        usage_context_workflow = UsageContext()
        usage_context_venue = UsageContext()

        usage_context_gender.valueCodeableConcept = CodeableConcept()
        usage_context_gender.code = Coding()
        usage_context_gender.code.code = "useContextGender"
        usage_context_gender.valueCodeableConcept = gender

        usage_context_age.valueCodeableConcept = CodeableConcept()
        usage_context_age.code = Coding()
        usage_context_age.code.code = "useContextAge"
        usage_context_age.valueCodeableConcept = age

        usage_context_workflow.valueCodeableConcept = CodeableConcept()
        usage_context_workflow.code = Coding()
        usage_context_workflow.code.code = "useContextWorkflow"
        usage_context_workflow.valueCodeableConcept = workflow

        usage_context_venue.valueCodeableConcept = CodeableConcept()
        usage_context_venue.code = Coding()
        usage_context_venue.code.code = "useContextVenue"
        usage_context_venue.valueCodeableConcept = venue

        if usage_context_workflow.valueCodeableConcept.coding[0].display == "":
            return [usage_context_gender, usage_context_age, usage_context_venue]
        elif usage_context_venue.valueCodeableConcept.coding[0].display == "":
            return [usage_context_gender, usage_context_age, usage_context_workflow]
        else:
            return [usage_context_gender, usage_context_age, usage_context_workflow, usage_context_venue]

    @classmethod
    def build_fhir_gender(cls, imis_activity_definition):
        male = cls.build_fhir_male(imis_activity_definition)
        female = cls.build_fhir_female(imis_activity_definition)
        if male == "":
            male = None
        if female == "":
            female = None

        codeable_concept = CodeableConcept()
        if male is not None:
            coding_male = Coding()
            coding_male.code = male
            coding_male.display = "Male"
            codeable_concept.coding.append(coding_male)
        if female is not None:
            coding_female = Coding()
            coding_female.code = female
            coding_female.display = "Female"
            codeable_concept.coding.append(coding_female)
            codeable_concept.text = "Male or Female"
        return codeable_concept

    @classmethod
    def build_fhir_age(cls, imis_activity_definition):
        adult = cls.build_fhir_adult(imis_activity_definition)
        kid = cls.build_fhir_kid(imis_activity_definition)
        if adult == "":
            adult = None
        if kid == "":
            kid = None

        codeable_concept = CodeableConcept()
        if adult is not None:
            coding_adult = Coding()
            coding_adult.code = adult
            coding_adult.display = "Adult"
            codeable_concept.coding.append(coding_adult)
        if kid is not None:
            coding_kid = Coding()
            coding_kid.code = kid
            coding_kid.display = "Kid"
            codeable_concept.coding.append(coding_kid)
            codeable_concept.text = "Adult or Kid"
        return codeable_concept

    @classmethod
    def build_fhir_venue(cls, imis_activity_definition):
        display = ""
        if imis_activity_definition.care_type == "O":
            display = "Out-patient"
        if imis_activity_definition.care_type == "I":
            display = "In-patient"
        if imis_activity_definition.care_type == "B":
            display = "Both"

        codeable_concept = CodeableConcept()
        #if imis_activity_definition.care_type is not None:
        coding_venue = Coding()
        coding_venue.code = imis_activity_definition.care_type
        coding_venue.display = display
        codeable_concept.coding.append(coding_venue)
        codeable_concept.text = "Clinical Venue"
        return codeable_concept

    @classmethod
    def build_fhir_workflow(cls, imis_activity_definition):
        display = ""
        if imis_activity_definition.category == "S":
            display = "Surgery"
        if imis_activity_definition.category == "C":
            display = "Consulation"
        if imis_activity_definition.category == "D":
            display = "Delivery"
        if imis_activity_definition.category == "A":
            display = "Antenatal"
        if imis_activity_definition.category == "O":
            display = "Other"

        codeable_concept = CodeableConcept()
        #if imis_activity_definition.category is not None:
        coding_workflow = Coding()
        coding_workflow.code = imis_activity_definition.category
        coding_workflow.display = display
        codeable_concept.coding.append(coding_workflow)
        codeable_concept.text = "Workflow Setting"
        return codeable_concept

    @classmethod
    def build_fhir_male(cls, imis_activity_definition):
        item_pat_cat = imis_activity_definition.patient_category
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
    def build_fhir_female(cls, imis_activity_definition):
        item_pat_cat = imis_activity_definition.patient_category
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
    def build_fhir_adult(cls, imis_activity_definition):
        item_pat_cat = imis_activity_definition.patient_category
        adult = ""
        if item_pat_cat > 8:
            kid = "K"
            item_pat_cat = item_pat_cat - 8
        if item_pat_cat >= 4:
            adult = "A"
        return adult

    @classmethod
    def build_fhir_kid(cls, imis_activity_definition):
        item_pat_cat = imis_activity_definition.patient_category
        kid = ""
        if item_pat_cat >= 8:
            kid = "K"
        return kid
