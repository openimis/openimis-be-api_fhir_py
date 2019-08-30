from api_fhir.models import DomainResource, Property, BackboneElement


class Contract(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)
    term = Property('term', 'BackboneElement')
