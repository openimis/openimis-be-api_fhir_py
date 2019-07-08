from api_fhir.models import Element, Property


class BackboneElement(Element):

    modifierExtension = Property('modifierExtension', 'Extension', count_max='*')
