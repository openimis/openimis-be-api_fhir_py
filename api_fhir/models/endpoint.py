from api_fhir.models import DomainResource, Property


class Endpoint(DomainResource):
    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str, required='*')
    connectionType = Property('connectionType', 'Coding', required=True)
    name = Property('name', str)
    managingOrganization = Property('managingOrganization', 'Reference')  # referencing `Organization`
    contact = Property('contact', 'ContactPoint', count_max='*')
    period = Property('period', 'Period')
    payloadType = Property('payloadType', 'CodeableConcept', required=True, count_max='*')
    payloadMimeType = Property('payloadMimeType', str, count_max='*')
    address = Property('address', str, required=True)
    header = Property('header', str, count_max='*')
