# Generated by Django 5.1.4 on 2025-01-13 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_department_employee_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compensation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='compensations',
            field=models.ManyToManyField(to='hr.compensation'),
        ),
    ]
