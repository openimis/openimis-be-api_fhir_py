from api_fhir_R4.models import Element, Property


class Signature(Element):

    type = Property('type', 'Coding', required=True, count_max='*')
    when = Property('when', 'FHIRDate', required=True)
    who = Property('who', 'Reference', required=True)  # referencing 'Practitioner', 'PractitionerRole', ...
    onBehalfOf = Property('onBehalfOf', 'Reference')  # referencing 'Practitioner', 'PractitionerRole', ...
    targetFormat = Property('targetFormat', str)
    sigFormat = Property('sigFormat', str)
    data = Property('data', str)
