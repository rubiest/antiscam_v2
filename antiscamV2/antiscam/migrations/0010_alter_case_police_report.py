# Generated by Django 4.2.3 on 2023-08-18 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antiscam', '0009_case_police_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='police_report',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]
