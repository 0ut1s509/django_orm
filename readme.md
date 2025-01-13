# pip install django django-extensions
# mete django-extensions nan installed_apps ki nan settings
psql -U postgres
Password for user postgres:

pip install python-decouple : pou nou pa mete enfo db a direkteman

kreye yon .env epi
DB_NAME=hr
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

anndan settings.py
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='default_db_name'),
        'USER': config('DB_USER', default='default_user'),
        'PASSWORD': config('DB_PASSWORD', default='default_password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

pip install psycopg2
python manage.py shell_plus --print-sql : pou nou lanse shell django a men avan nap bezwen enstale django_extensions

egzanp anrejistreman done nan shell la :
>>> e = Employee(first_name='John',last_name='Doe')
>>> e.save()
INSERT INTO "hr_employee" ("first_name", "last_name")
VALUES ('John', 'Doe') RETURNING "hr_employee"."id"
Execution time: 0.003234s [Database: default]

Employee.objects.all() : seleksyone tout antre tab la
e = Employee.objects.get(id=1) rekipere antre ki gen id 1 an
Employee.objects.filter(first_name='Jane') rekipere antre ki gen firstname = jane
 e.delete() : efase antre ki t seleksyone a


 # OneToOneField(to, on_delete, parent_link=False, **options)
 >>> c = Contact(phone='40812345678', address='101 N 1st Street, San Jose, CA')
>>> c.save()
>>> e.contact = c
>>> e.save()
nou k aksede Employee apati de Contact(c.employee) vice versa(e.contact)

>>> Employee.objects.select_related('contact').all() : si nou ta vle aksede epi afiche anplwaye a ak tout kontak li nan yon paj

# One-To-Many Relationship
>>> d = Department(name='IT',description='Information Technology')
>>> d.save()
>>> e = Employee(first_name='John',last_name='Doe',department=d)
>>> e.save()
>>> e = Employee(first_name='Jane',last_name='Doe',department=d)
>>> e.save()
>>> e.department 
<Department: IT>
>>> e.department.description
'Information Technology'
seleksyone tout anplwaye ki nan yon depatman 
 d.employee_set.all()
 Employee.objects.select_related('department').all() : si nou ta vle aksede epi afiche anplwaye a ak tout depatman li nan yon paj
