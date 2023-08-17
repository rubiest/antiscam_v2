# Generated by Django 4.2.3 on 2023-08-17 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antiscam', '0008_customuser_old_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scammer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('brief_intro', models.CharField(max_length=255)),
                ('modus_operandi', models.TextField(default='')),
                ('is_verified', models.BooleanField(default=False)),
                ('date_reported', models.DateField(default='')),
                ('last_date_reported', models.DateField(default='')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
