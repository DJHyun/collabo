# Generated by Django 2.1.8 on 2019-05-13 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('momo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='audiChange',
            field=models.FloatField(),
        ),
    ]
