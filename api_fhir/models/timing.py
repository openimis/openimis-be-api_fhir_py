from api_fhir.models import Element, Property


class TimingRepeat(Element):

    boundsDuration = Property('boundsDuration', 'Duration')
    boundsPeriod = Property('boundsPeriod', 'Period')
    boundsRange = Property('boundsRange', 'Range')
    count = Property('count', int)
    countMax = Property('countMax', int)
    dayOfWeek = Property('dayOfWeek', str, count_max='*')  # mon | tue | wed | thu | fri | sat | sun
    duration = Property('duration', float)
    durationMax = Property('durationMax', float)
    durationUnit = Property('durationUnit', str)  # s | min | h | d | wk | mo | a - unit of time (UCUM)
    frequency = Property('frequency', int)
    frequencyMax = Property('frequencyMax', int)
    offset = Property('offset', int)
    period = Property('period', float)
    periodMax = Property('periodMax', float)
    periodUnit = Property('periodUnit', str)  # s | min | h | d | wk | mo | a - unit of time (UCUM)
    timeOfDay = Property('timeOfDay', 'FHIRDate', count_max='*')
    when = Property('when', str, count_max='*')


class Timing(Element):

    code = Property('code', 'CodeableConcept')  # BID | TID | QID | AM | PM | QD | QOD | Q4H | Q6H +
    event = Property('event', 'FHIRDate', count_max='*')
    repeat = Property('repeat', 'TimingRepeat')
