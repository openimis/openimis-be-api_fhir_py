from api_fhir_R4.models import Element, Property


class Meta(Element):

    versionId = Property('versionId', str)
    lastUpdated = Property('lastUpdated', 'FHIRDate')
    source = Property('source', str)
    profile = Property('profile', str, count_max='*')
    security = Property('security', 'Coding', count_max='*')
    tag = Property('tag', 'Coding', count_max='*')
