from api_fhir.models import FHIRBaseObject, Property


class Element(FHIRBaseObject):

    id = Property('id', str)
    extension = Property('extension', 'Extension', count_max='*')

    class Meta:
        app_label = 'api_fhir'
