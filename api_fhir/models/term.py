from api_fhir.models import DomainResource, Property, BackboneElement


class Term(BackboneElement):

    identifier = Property('identifier', 'Identifier', count_max='*')
    applies = Property('applies', 'Period')