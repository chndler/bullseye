# Generated by Django 2.0.5 on 2018-05-24 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bullseye', '0004_auto_20180524_1256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'permissions': (('view_student', 'View Student'),)},
        ),
    ]
