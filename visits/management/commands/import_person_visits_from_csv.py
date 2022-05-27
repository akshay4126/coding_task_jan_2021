from django.core.management.base import BaseCommand, CommandError
from visits.models import Person, Location, Visit
from sentiance.settings import VISIT_LOC_MAX_LEVEL, VISIT_LOC_MIN_LEVEL
from geolib import geohash
from visits.utils import latlon2gcodes
import csv

# Next 3 TODO
# 1:
# 2:
# 3:

CSV_DELIMITER = ';'
# DATE FORMAT string for YYYYMMddHHmmZ
DATE_FORMAT = '%Y%m%d%H%M%S%z'


class Command(BaseCommand):
    help = 'Loads Visits data from Persons CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_data_file')
        parser.add_argument('person')

    def handle(self, *args, **options):
        csv_path = options['csv_data_file']
        # TODO: expecting csv_file name as 'person.id.csv'
        person_id = options['person']

        if person_id is None:
            raise CommandError('Can not parse person_id')

        person, created = Person.objects.get_or_create(person_id=person_id)

        self.stdout.write('Starting to import: %s\n' % csv_path)
        with open(csv_path) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            csvheader = next(csvreader)
            count = 0
            for row in csvreader:
                latitude, longitude = float(row[0]), float(row[1])
                gcodes = latlon2gcodes(latitude, longitude)
                for gcode, level in gcodes:
                    # gcode = geohash.encode(latitude, longitude, VISIT_LOC_MIN_LEVEL)
                    centeroid = geohash.decode(gcode)
                    latitude, longitude = centeroid.lat, centeroid.lon
                    temp_location = {
                        'latitude': latitude,
                        'longitude': longitude,
                        'level': level,
                        'gcode': gcode
                    }
                    location, created = Location.objects.get_or_create(**temp_location)

                    temp_visit = {
                        'location': location,
                        'person': person,
                    }
                    visit, created = Visit.objects.get_or_create(**temp_visit)
                    if created:
                        visit.visit_count = 1
                    else:
                        visit.visit_count += 1
                    visit.save()

                count += 1
                if count % 20 == 0:
                    self.stdout.write('Imported {} records for {}'.format(count,person))
            self.stdout.write('Imported {} visits for {} from {}'.format(count,person,csv_path))
