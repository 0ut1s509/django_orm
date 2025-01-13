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

 # Many-to-Many Relationship

class Compensation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    contact = models.OneToOneField(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    compensations = models.ManyToManyField(Compensation)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

 >>> c1 = Compensation(name='Stock')
>>> c1.save()
>>> c2 = Compensation(name='Bonuses') 
>>> c2.save()
>>> c3 = Compensation(name='Profit Sharing')  
>>> c3.save()
>>> Compensation.objects.all()
<QuerySet [<Compensation: Stock>, <Compensation: Bonuses>, <Compensation: Profit Sharing>]>
bay anplwaye konpansasyon
>>> e.compensations.add(c1)
>>> e.compensations.add(c2) 
>>> e.save()
aksede tout konpansasyon yon anplwaye
>>> e.compensations.all()
<QuerySet [<Compensation: Stock>, <Compensation: Bonuses>]>

>>> e = Employee.objects.filter(first_name='Jane',last_name='Doe').first()
>>> e 
<Employee: Jane Doe>
>>> e.compensations.add(c1)
>>> e.compensations.add(c2) 
>>> e.compensations.add(c3) 
>>> e.save()
>>> e.compensations.all()
<QuerySet [<Compensation: Stock>, <Compensation: Bonuses>, <Compensation: Profit Sharing>]>
seleksyone tout anplwaye ki gen konpansasyon c1
>>> c1
<Compensation: Stock>
>>> c1.employee_set.all()
<QuerySet [<Employee: John Doe>, <Employee: Jane Doe>]>

retire konpansasyon anplwaye
>>> e = Employee.objects.filter(first_name='Jane',last_name='Doe').first()
>>> e                                                                     
<Employee: Jane Doe>
>>> e.compensations.remove(c3)
>>> e.save()

efase tout anplwaye c3 : c3.employee_set.clear()

# ManyToManyField Through
class Job(models.Model):
    title = models.CharField(max_length=255)
    employees = models.ManyToManyField(Employee, through='Assignment')

    def __str__(self):
        return self.title


class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Job, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField(default=date(9999, 12, 31))


>>> j1 = Job(title='Software Engineer I')
>>> j1.save()
>>> j2 = Job(title='Software Engineer II') 
>>> j2.save() 
>>> j3 = Job(title='Software Engineer III')
>>> j3.save()
>>> Job.objects.all()
<QuerySet [<Job: Software Engineer I>, <Job: Software Engineer II>, <Job: Software Engineer III>]>

>>> e1 = Employee.objects.filter(first_name='John',last_name='Doe').first()
>>> e1
<Employee: John Doe>
>>> e2 = Employee.objects.filter(first_name='Jane', last_name='Doe').first()
>>> e2
<Employee: Jane Doe>

>>> from datetime import date
>>> a1 = Assignment(employee=e1,position=j1, begin_date=date(2019,1,1), end_date=date(2021,12,31))
>>> a1.save()
>>> a2 = Assignment(employee=e1,position=j2, begin_date=date(2022,1,1))
>>> a2.save()
>>> a3 = Assignment(employee=e2, position=j1, begin_date=date(2019, 3, 1))
>>> a3.save()

retire enstans nan model entemedye a
>>> j2.employees.remove(e2) 
retire tout anplwaye pou j1
>>> j1.employees.clear() 


# Django Limit Offset
seleksyone 10 premye eleman : Entity.objects.all()[:10] sinou vle odone apati de yon chan Entity.objects.all().order_by(field_name)[:10]

seleksyone soti nan 10 rive nan 20 : Entity.objects.all().order_by(field_name)[10:20]
django pa sipote endeksasyon negative : Entity.objects.all().order_by(field_name)[-10]

# Django LIKE
field_name__startswith : verifye si yon chan komanse pa tel ou tel karakte 
Employee.objects.filter(first_name__startswith='Je') 
Employee.objects.filter(first_name__istartswith='je') : san teni kont de majiskil ak miniskil

field_name__endswith  : verifye si yon chan fini pa tel ou tel karakte
Employee.objects.filter(first_name__endswith='er') 
Employee.objects.filter(first_name__iendswith='ER') san teni kont de majiskil miniskil 

field_name__contains : verifye si yon genyen tel ou tel karakte 
 Employee.objects.filter(first_name__contains='ff')  
 Employee.objects.filter(first_name__icontains='ff') : san teni kont de majiskil ak miniskil
