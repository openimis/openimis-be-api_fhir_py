from api_fhir_R4.models import Property, Resource


class DomainResource(Resource):

    contained = Property('contained', Resource, count_max='*')
    extension = Property('extension', 'Extension', count_max='*')
    modifierExtension = Property('modifierExtension', 'Extension', count_max='*')
    text = Property('text', 'Narrative')
