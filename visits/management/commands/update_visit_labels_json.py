from django.core.management.base import BaseCommand, CommandError
from visits.models import Person, Location, Visit
import json

class Command(BaseCommand):
    help = 'Loads Computed Visit labels from json file'

    def add_arguments(self, parser):
        parser.add_argument('json_visit_labels_file')

    def handle(self, *args, **options):
        json_path = options['json_visit_labels_file']

        try:
            with open(json_path) as f:
                json_data = json.load(f)
                for person_visit_data in json_data:
                    person_id = person_visit_data['person_id']
                    person = Person.objects.get(person_id=person_id)
                    if not person:
                        raise CommandError('Cannot find {} in Person table'.format(person_id))
                    for visit_label in person_visit_data['visit_labels']:

                        location = Location.objects.get(gcode=visit_label['gcode'])
                        visit = Visit.objects.get(person=person, location=location)
                        visit.visit_label = visit_label['label']
                        self.stdout.write('{} {} {}'.format(person_id, visit_label, location))
                        visit.save()
        except CommandError as ce:
            self.stdout.write('Error in loading label data from json file', ce)