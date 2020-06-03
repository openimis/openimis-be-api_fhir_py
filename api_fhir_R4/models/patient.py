from api_fhir_R4.models import BackboneElement, DomainResource, Property


class PatientContact(BackboneElement):

    relationship = Property('relationship', 'CodeableConcept', count_max='*')
    name = Property('name', 'HumanName')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    address = Property('address', 'Address')
    gender = Property('gender', str)  # male | female | other | unknown
    organization = Property('organization', 'Reference')  # referencing 'Organization'
    period = Property('period', 'Period')


class PatientCommunication(BackboneElement):

    language = Property('language', 'CodeableConcept', required=True)
    preferred = Property('preferred', bool)


class PatientLink(BackboneElement):

    other = Property('other', 'Reference', required=True)  # referencing 'Patient' and 'RelatedPerson'
    type = Property('type', str, required=True)  # replaced-by | replaces | refer | seealso


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
    communication = Property('communication', 'PatientCommunication', count_max='*')
    generalPractitioner = Property('generalPractitioner', 'Reference', count_max='*')  # referencing `Organization, Practitioner`
    managingOrganization = Property('managingOrganization', 'Reference')  # referencing `Organization`
    link = Property('link', 'PatientLink', count_max='*')
