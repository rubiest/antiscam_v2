# Generated by Django 4.2.3 on 2023-08-16 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antiscam', '0004_customuser_phone_number_customuser_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='state',
            new_name='location',
        ),
    ]
