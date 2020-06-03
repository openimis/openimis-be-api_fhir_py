from api_fhir_R4.models import Element, Property, BackboneElement


class TimingRepeat(Element):

    boundsDuration = Property('boundsDuration', 'Duration')
    boundsRange = Property('boundsRange', 'Range')
    boundsPeriod = Property('boundsPeriod', 'Period')
    count = Property('count', int)
    countMax = Property('countMax', int)
    duration = Property('duration', float)
    durationMax = Property('durationMax', float)
    durationUnit = Property('durationUnit', str)  # s | min | h | d | wk | mo | a - unit of time (UCUM)
    frequency = Property('frequency', int)
    frequencyMax = Property('frequencyMax', int)
    period = Property('period', float)
    periodMax = Property('periodMax', float)
    periodUnit = Property('periodUnit', str)  # s | min | h | d | wk | mo | a - unit of time (UCUM)
    dayOfWeek = Property('dayOfWeek', str, count_max='*')  # mon | tue | wed | thu | fri | sat | sun
    timeOfDay = Property('timeOfDay', 'FHIRDate', count_max='*')
    when = Property('when', str, count_max='*')
    offset = Property('offset', int)


class Timing(BackboneElement):

    event = Property('event', 'FHIRDate', count_max='*')
    repeat = Property('repeat', 'TimingRepeat')
    code = Property('code', 'CodeableConcept')  # BID | TID | QID | AM | PM | QD | QOD | Q4H | Q6H +
