from ariadne import convert_kwargs_to_snake_case
from django.core.exceptions import ObjectDoesNotExist

from visits.models import Person, Location, Visit
from geolib import geohash
from sentiance.settings import VISIT_LOC_MIN_LEVEL, VISIT_LOC_MAX_LEVEL


@convert_kwargs_to_snake_case
def resolve_persons(*_):
    return Person.objects.all()


@convert_kwargs_to_snake_case
def resolve_person(*_, id):
    person = None
    # TODO: move this code in the model
    if id is not None:
        try:
            person = Person.objects.get(pk=id)
        except ObjectDoesNotExist:
            pass
    return person


@convert_kwargs_to_snake_case
def resolve_locations(*_, level):
    return Location.objects.filter(level=level)


@convert_kwargs_to_snake_case
def resolve_location(*_, id):
    location = None
    # TODO: move this code in the model
    if id is not None:
        try:
            location = Location.objects.get(pk=id)
        except ObjectDoesNotExist:
            pass
    return Location


@convert_kwargs_to_snake_case
def resolve_sample_visits(*_, visit_label):
    visits = []
    if visit_label:
        visits = Visit.objects.filter(visit_label=visit_label)
    else:
        visits = Visit.objects.all()
    # TODO: use pagination, or a configurable constant
    return visits[:10]


@convert_kwargs_to_snake_case
def resolve_person_visit(*_, person_id, lat, lon, level):
    visit = None
    if level < VISIT_LOC_MIN_LEVEL:
        return {'visit': None,
                'message': "The precision level={}, is too broad. "
                           "Try a value between {} and {}".format(level, VISIT_LOC_MIN_LEVEL, VISIT_LOC_MAX_LEVEL)}
    if level > VISIT_LOC_MAX_LEVEL:
        return {'visit': None,
                'message': "The precision level={}, is too narrow. "
                           "Try a value between {} and {}".format(level, VISIT_LOC_MIN_LEVEL, VISIT_LOC_MAX_LEVEL)}
    try:
        person = Person.objects.get(id=person_id)
        gcode = geohash.encode(lat, lon, level)
        location = Location.objects.get(gcode=gcode)
        visit = Visit.objects.filter(person=person, location=location)
        # print(gcode, person, location, visit)

    except Exception as ex:
        print('Error fetching person visit details, {} {} {} {}'
              .format(person_id, lat, lon, level), ex)
        return {'visit': None, 'message': "No visit records found for person {}, "
                                          "for the given location information.".format(person_id)}
    if visit:
        return {'visit': visit[0], 'message': str(visit[0])}
    else:
        return {'visit': None, 'message': "No visit records found for person {}, "
                                          "for the given location information.".format(person_id)}
