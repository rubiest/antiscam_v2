# Generated by Django 4.2.3 on 2023-08-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antiscam', '0007_customuser_profile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='old_email',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]