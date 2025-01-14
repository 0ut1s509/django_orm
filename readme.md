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

 # Django In
 field_name IN (v1, v2, ...) verifye si chan fe pati de yon lis kelkonk
 Employee.objects.filter(department_id__in=(1,2,3)) : seleksyone anplwaye ke id depatman egal 1,2 oubyen 3
 departments = Department.objects.filter(Q(name='Sales') | Q(name='Marketing')) : seleksyone ki egal a Sales oubyen Marketing
 Employee.objects.filter(department__in=departments) : selesyone anplwaye ki fe pati de reket presedan

 field_name NOT IN (v1, v2, ...) : verifye si chan pa fe pati de yon lis kelkonk
 Employee.objects.filter(~Q(department_id__in=(1,2,3))) seleksyone anplwaye ke id depatman pa egal 1,2 oubyen 3
 Employee.objects.exclude(department_id__in=(1,2,3)) 

 # Django range
 field_name BETWEEN low_value AND high_value
 field_name >= low_value AND field_name <= high_value
 Entity.objects.filter(field_name__range=(low_value,high_value))
 >>> Employee.objects.filter(id__range=(1,5))
  Assignment.objects.filter(begin_date__range=(start_date,end_date))  

  NOT BETWEEN
  Entity.objects.filter(~Q(field_name__range=(low_value,high_value)))
  Employee.objects.filter(~Q(id__range=(1,5)))

  # Django exists
  >>> Employee.objects.filter(first_name__startswith='J').exists()
SELECT 1 AS "a"
  FROM "hr_employee"
 WHERE "hr_employee"."first_name"::text LIKE 'J%'
 LIMIT 1
Execution time: 0.000000s [Database: default]
True

# Django Aggregate
 Employee.objects.count() : count() kontrole konbyen kantite anplwaye ki genyen
 >>> Employee.objects.count()
SELECT COUNT(*) AS "__count"
  FROM "hr_employee"        
Execution time: 0.002160s [Database: default]
220

>>> Employee.objects.filter(first_name__startswith='J').count()
SELECT COUNT(*) AS "__count"
  FROM "hr_employee"
 WHERE "hr_employee"."first_name"::text LIKE 'J%'
Execution time: 0.000000s [Database: default]
29
# MAX
>>> Employee.objects.aggregate(Max('salary'))
SELECT MAX("hr_employee"."salary") AS "salary__max"
  FROM "hr_employee"
Execution time: 0.002001s [Database: default]
{'salary__max': Decimal('248312.00')}

# Min
>>> Employee.objects.aggregate(Min('salary')) 
SELECT MIN("hr_employee"."salary") AS "salary__min"
  FROM "hr_employee"
Execution time: 0.002015s [Database: default]
{'salary__min': Decimal('40543.00')}   

# Avg
>>> Employee.objects.aggregate(Avg('salary')) 
SELECT AVG("hr_employee"."salary") AS "salary__avg"
  FROM "hr_employee"
Execution time: 0.005468s [Database: default]
{'salary__avg': Decimal('137100.490909090909')}

# sum
>>> Employee.objects.aggregate(Sum('salary')) 
SELECT SUM("hr_employee"."salary") AS "salary__sum"
  FROM "hr_employee"
Execution time: 0.000140s [Database: default]
{'salary__sum': Decimal('30162108.00')}

# Django Group By
## group by with count
>>> (Employee.objects
     .values('department')
     .annotate(head_count=Count('department'))
     .order_by('department')
  )
SELECT "hr_employee"."department_id",
       COUNT("hr_employee"."department_id") AS "head_count"
  FROM "hr_employee"
 GROUP BY "hr_employee"."department_id"
 ORDER BY "hr_employee"."department_id" ASC
 LIMIT 21
Execution time: 0.001492s [Database: default]
<QuerySet [{'department': 1, 'head_count': 30}, {'department': 2, 'head_count': 40}, {'department': 3, 'head_count': 28}, {'department': 4, 'head_count': 29}, {'department': 5, 'head_count': 29}, {'department': 6, 'head_count': 30}, {'department': 7, 'head_count': 34}]>

## Django Group By with Sum example
>>> (Employee.objects
...     .values('department')
...     .annotate(total_salary=Sum('salary'))
...     .order_by('department')
...  )
SELECT "hr_employee"."department_id",
       SUM("hr_employee"."salary") AS "total_salary"
  FROM "hr_employee"
 GROUP BY "hr_employee"."department_id"
 ORDER BY "hr_employee"."department_id" ASC
 LIMIT 21
Execution time: 0.000927s [Database: default]
<QuerySet [{'department': 1, 'total_salary': Decimal('3615341.00')}, {'department': 2, 'total_salary': Decimal('5141611.00')}, {'department': 3, 'total_salary': Decimal('3728988.00')}, {'department': 4, 'total_salary': Decimal('3955669.00')}, {'department': 5, 'total_salary': Decimal('4385784.00')}, {'department': 6, 'total_salary': Decimal('4735927.00')}, {'department': 7, 'total_salary': Decimal('4598788.00')}]>


##  Django Group By with Min, Max, and Avg example
>>> (Employee.objects
...     .values('department')
...     .annotate(
...         min_salary=Min('salary'),
...         max_salary=Max('salary'),
...         avg_salary=Avg('salary')
...     )
...     .order_by('department')
...  )
SELECT "hr_employee"."department_id",
       MIN("hr_employee"."salary") AS "min_salary",
       MAX("hr_employee"."salary") AS "max_salary",
       AVG("hr_employee"."salary") AS "avg_salary"
  FROM "hr_employee"
 GROUP BY "hr_employee"."department_id"
 ORDER BY "hr_employee"."department_id" ASC
 LIMIT 21
Execution time: 0.001670s [Database: default]
<QuerySet [{'department': 1, 'min_salary': Decimal('45427.00'), 'max_salary': Decimal('149830.00'), 'avg_salary': Decimal('120511.366666666667')}, {'department': 
2, 'min_salary': Decimal('46637.00'), 'max_salary': Decimal('243462.00'), 'avg_salary': Decimal('128540.275000000000')}, {'department': 3, 'min_salary': Decimal('40762.00'), 'max_salary': Decimal('248265.00'), 'avg_salary': Decimal('133178.142857142857')}, {'department': 4, 'min_salary': Decimal('43000.00'), 'max_salary': 
Decimal('238016.00'), 'avg_salary': Decimal('136402.379310344828')}, {'department': 5, 'min_salary': Decimal('42080.00'), 'max_salary': Decimal('246403.00'), 'avg_salary': Decimal('151233.931034482759')}, {'department': 6, 'min_salary': Decimal('58356.00'), 'max_salary': Decimal('248312.00'), 'avg_salary': Decimal('157864.233333333333')}, {'department': 7, 'min_salary': Decimal('40543.00'), 'max_salary': Decimal('238892.00'), 'avg_salary': Decimal('135258.470588235294')}]>

## Django group by with join example
>>> (Department.objects
...     .values('name')
...     .annotate(
...         head_count=Count('employee')
...     )
...  )
SELECT "hr_department"."name",
       COUNT("hr_employee"."id") AS "head_count"
  FROM "hr_department"
  LEFT OUTER JOIN "hr_employee"
    ON ("hr_department"."id" = "hr_employee"."department_id")
 GROUP BY "hr_department"."name"
 LIMIT 21
Execution time: 0.001953s [Database: default]
<QuerySet [{'name': 'Marketing', 'head_count': 28}, {'name': 'Finance', 'head_count': 29}, {'name': 'SCM', 'head_count': 29}, {'name': 'GA', 'head_count': 30}, {'name': 'Sales', 'head_count': 40}, {'name': 'IT', 'head_count': 30}, {'name': 'HR', 'head_count': 34}]>


## Django group by with having
>>> (Department.objects
...     .values('name')
...     .annotate(
...         head_count=Count('employee')
...     )
...     .filter(head_count__gt=30)
...  )
SELECT "hr_department"."name",
       COUNT("hr_employee"."id") AS "head_count"
  FROM "hr_department"
  LEFT OUTER JOIN "hr_employee"
    ON ("hr_department"."id" = "hr_employee"."department_id")
 GROUP BY "hr_department"."name"
HAVING COUNT("hr_employee"."id") > 30
 LIMIT 21
Execution time: 0.002893s [Database: default]
<QuerySet [{'name': 'Sales', 'head_count': 40}, {'name': 'HR', 'head_count': 34}]>

# Django isnull
verifye si yon chan manke 

Entity.objects.filter(field_name__isnull=True)
>>> Employee.objects.filter(contact_id__isnull=True)
SELECT "hr_employee"."id",
       "hr_employee"."first_name",
       "hr_employee"."last_name",
       "hr_employee"."contact_id",
       "hr_employee"."department_id"
  FROM "hr_employee"
 WHERE "hr_employee"."contact_id" IS NULL

 >>> Employee.objects.filter(contact_id__isnull=False) 
SELECT "hr_employee"."id",
       "hr_employee"."first_name",
       "hr_employee"."last_name",
       "hr_employee"."contact_id",
       "hr_employee"."department_id"
  FROM "hr_employee"
 WHERE "hr_employee"."contact_id" IS NOT NULL
