# Generated by Django 4.2.3 on 2023-08-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antiscam', '0008_case_reported_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='police_report',
            field=models.BooleanField(default=False),
        ),
    ]