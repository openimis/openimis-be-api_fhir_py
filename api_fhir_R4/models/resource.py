from api_fhir_R4.models import FHIRBaseObject, Property


class Resource(FHIRBaseObject):

    id = Property('id', str)
    meta = Property('meta', 'Meta')
    implicitRules = Property('implicitRules', str)
    language = Property('language', str)  # code
