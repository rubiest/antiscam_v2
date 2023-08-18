# Generated by Django 4.2.3 on 2023-08-18 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('antiscam', '0007_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='reported_by',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]