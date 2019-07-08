from api_fhir.models import Element, Property


class Signature(Element):

    blob = Property('blob', str)
    contentType = Property('contentType', str)
    onBehalfOfReference = Property('onBehalfOfReference', 'Reference')  # referencing `Practitioner, RelatedPerson, Patient, Device, Organization`
    onBehalfOfUri = Property('onBehalfOfUri', str)
    type = Property('type', 'Coding', count_max='*')
    when = Property('when', 'FHIRDate')
    whoReference = Property('whoReference', 'Reference')  # referencing `Practitioner, RelatedPerson, Patient, Device, Organization`
    whoUri = Property('whoUri', str)
