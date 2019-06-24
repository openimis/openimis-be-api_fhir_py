from api_fhir.models import FHIRBaseObject, Property


class Resource(FHIRBaseObject):

    id = Property('id', str)
    meta = Property('meta', 'Meta')
    implicitRules = Property('implicitRules', str)
    language = Property('language', str)  # code

    class Meta:
        app_label = 'api_fhir'
