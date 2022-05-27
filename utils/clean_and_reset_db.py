import os
from pathlib import Path

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rivm2016.settings')
BASE_DIR = Path(__file__).resolve().parent.parent

print('This script is for demo only')
print('This script will:\n'
      'a) Remove existing migration files.\n'
      'b) Delete db.sqlite3.\n'
      'c) Make database migrations.\n'
      'd) Run database migrate.\n'
      'e) Load seed data.\n')
response = input("Do you wish to continue? (y/n) ")
if response.lower() == 'y':
    print('Removing ...')
    os.system('find %s -path "*/migrations/*.py" -not -name "__init__.py" -exec rm -vf {} \;' % BASE_DIR)
    os.system('find %s -path "*/migrations/*.pyc" -exec rm -vf {} \;' % BASE_DIR)
    os.system('rm -vf ./db.sqlite3')

    print('\nClean up done. Running migrations\n\n')
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    print('\n\n Loading data from person.[1,2,3].csv .\n')
    os.system('python manage.py import_person_visits_from_csv data/person.1.csv person.1')
    os.system('python manage.py import_person_visits_from_csv data/person.2.csv person.2')
    os.system('python manage.py import_person_visits_from_csv data/person.3.csv person.3')
    print('\nDone.\n\n')
    print('\nNow you can start the server with following command.\n\n')
    print('\npython manage.py runserver 0.0.0.0:8000\n\n')
