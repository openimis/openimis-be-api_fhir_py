from api_fhir.models import BackboneElement, DomainResource, Property


class PatientContact(BackboneElement):

    address = Property('address', 'Address')
    gender = Property('gender', str)  # male | female | other | unknown
    name = Property('name', 'HumanName')
    organization = Property('organization', 'Reference')
    period = Property('period', 'Period')
    relationship = Property('relationship', 'CodeableConcept', count_max='*')
    telecom = Property('telecom', 'ContactPoint', count_max='*')

    class Meta:
        app_label = 'api_fhir'


class PatientAnimal(BackboneElement):

    breed = Property('breed', 'CodeableConcept')
    genderStatus = Property('genderStatus', 'CodeableConcept')
    species = Property('species', 'CodeableConcept')

    class Meta:
        app_label = 'api_fhir'


class PatientCommunication(BackboneElement):

    language = Property('language', 'CodeableConcept')
    preferred = Property('preferred', bool)

    class Meta:
        app_label = 'api_fhir'


class PatientLink(BackboneElement):

    other = Property('other', 'Reference')
    type = Property('type', str)  # replaced-by | replaces | refer | seealso

    class Meta:
        app_label = 'api_fhir'


class Patient(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    active = Property('active', bool)
    name = Property('name', 'HumanName', count_max='*')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    gender = Property('gender', str)  # (male | female | other | unknown)
    birthDate = Property('birthDate', 'FHIRDate')
    deceasedBoolean = Property('deceasedBoolean', bool)
    deceasedDateTime = Property('deceasedDateTime', 'FHIRDate')
    address = Property('address', 'Address', count_max='*')
    maritalStatus = Property('maritalStatus', 'CodeableConcept')
    multipleBirthBoolean = Property('multipleBirthBoolean', bool)
    multipleBirthInteger = Property('multipleBirthInteger', int)
    photo = Property('photo', 'Attachment', count_max='*')
    contact = Property('contact', 'PatientContact', count_max='*')
    animal = Property('animal', 'PatientAnimal')
    communication = Property('communication', 'PatientCommunication', count_max='*')
    generalPractitioner = Property('generalPractitioner', 'Reference', count_max='*')  # referencing `Organization, Practitioner`
    managingOrganization = Property('managingOrganization', 'Reference')  # referencing `Organization`
    link = Property('link', 'PatientLink')

    class Meta:
        app_label = 'api_fhir'
