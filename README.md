Rice Bikes Processing App
=========================

This site is built for use by the employees of Rice Bikes, the student-
run bike shop at Rice University.

Before running the app, you must fill in the secret key and email credentials in app/mysite/settings.py.

TO RUN THE APP:
Execute the following shell commands.


1. source venv/bin/activate

2. python manage.py makemigrations

3. python manage.py migrate

4. python manage.py createsuperuser

5. ./seed_all_menus.sh

6. python manage.py runserver
