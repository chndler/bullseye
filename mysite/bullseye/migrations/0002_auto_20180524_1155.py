# Generated by Django 2.0.5 on 2018-05-24 16:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bullseye', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='object_id',
            field=models.CharField(default=uuid.uuid4, max_length=50, null=True),
        ),
    ]
