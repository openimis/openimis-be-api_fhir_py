from api_fhir.models.backboneElement import BackboneElement
from api_fhir.models.domainResource import DomainResource


class Patient(DomainResource):

    resource_type = "Patient"

    def __init__(self):
        self.identifier = None  # List of `Identifier` items (represented as `dict` in JSON).

        self.active = None  # Type `bool`.

        self.name = None  # List of `HumanName` items (represented as `dict` in JSON).

        self.telecom = None  # List of `ContactPoint` items (represented as `dict` in JSON).

        self.gender = None  # Type `str` (male | female | other | unknown).

        self.birthDate = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.deceasedBoolean = None  # Type `bool`.

        self.deceasedDateTime = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.address = None  # List of `Address` items (represented as `dict` in JSON).

        self.maritalStatus = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.multipleBirthBoolean = None  # Type `bool`.

        self.multipleBirthInteger = None  # Type `int`.

        self.photo = None  # List of `Attachment` items (represented as `dict` in JSON).

        self.contact = None  # List of `PatientContact` items (represented as `dict` in JSON).

        self.animal = None  # Type `PatientAnimal` (represented as `dict` in JSON).

        self.communication = None  # List of `PatientCommunication` items (represented as `dict` in JSON).

        self.generalPractitioner = None  # List of `Reference` items referencing `Organization, Practitioner` (represented as `dict` in JSON).

        self.managingOrganization = None  # Type `Reference` referencing `Organization` (represented as `dict` in JSON).

        self.link = None  # List of `PatientLink` items (represented as `dict` in JSON).

        super(Patient, self).__init__()

    class Meta:
        app_label = 'api_fhir'


class PatientContact(BackboneElement):

    resource_type = "PatientContact"

    def __init__(self):

        self.address = None  # Type `Address` (represented as `dict` in JSON).

        self.gender = None  # Type `str` (male | female | other | unknown)

        self.name = None  # Type `HumanName` (represented as `dict` in JSON).

        self.organization = None  # Type `Reference` (represented as `dict` in JSON).

        self.period = None  # Type `Period` (represented as `dict` in JSON).

        self.relationship = None  # List of `CodeableConcept` items (represented as `dict` in JSON).

        self.telecom = None  # List of `ContactPoint` items (represented as `dict` in JSON).

        super(PatientContact, self).__init__()

    class Meta:
        app_label = 'api_fhir'


class PatientAnimal(BackboneElement):

    resource_type = "PatientAnimal"

    def __init__(self):
        self.breed = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.genderStatus = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.species = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        super(PatientAnimal, self).__init__()

    class Meta:
        app_label = 'api_fhir'


class PatientCommunication(BackboneElement):

    resource_type = "PatientCommunication"

    def __init__(self):
        self.language = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.preferred = None  # Type `bool`.

        super(PatientCommunication, self).__init__()

    class Meta:
        app_label = 'api_fhir'


class PatientLink(BackboneElement):

    resource_type = "PatientLink"

    def __init__(self):
        self.other = None  # Type `FHIRReference` (represented as `dict` in JSON).

        self.type = None  # Type `str` (replaced-by | replaces | refer | seealso).

        super(PatientLink, self).__init__()

    class Meta:
        app_label = 'api_fhir'
