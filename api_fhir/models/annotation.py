from api_fhir.models import Element, Property


class Annotation(Element):

    authorReference = Property('authorReference', 'Reference')
    authorString = Property('authorString', str)
    text = Property('text', str)
    time = Property('time', 'FHIRDate')
