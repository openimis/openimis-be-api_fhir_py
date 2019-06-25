from api_fhir.models import DomainResource, Property, BackboneElement


class PractitionerQualification(BackboneElement):
    identifier = Property('identifier', 'Identifier', count_max='*')
    code = Property('code', 'CodeableConcept', required=True)
    period = Property('period', 'Period')
    issuer = Property('issuer', 'Reference')  # referencing `Organization`


class Practitioner(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    active = Property('active', bool)
    name = Property('name', 'HumanName', count_max='*')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    address = Property('address', 'Address', count_max='*')
    gender = Property('gender', str)  # AdministrativeGender
    birthDate = Property('birthDate', 'FHIRDate')
    photo = Property('photo', 'Attachment', count_max='*')
    qualification = Property('qualification', 'PractitionerQualification', count_max='*')
    communication = Property('communication', 'CodeableConcept', count_max='*')
