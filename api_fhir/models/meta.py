from api_fhir.models import Element, Property


class Meta(Element):

    lastUpdated = Property('lastUpdated', 'FHIRDate')
    profile = Property('profile', str, count_max='*')
    security = Property('security', 'Coding', count_max='*')
    tag = Property('tag', 'Coding', count_max='*')
    versionId = Property('versionId', str)
