# Generated by Django 2.1.8 on 2019-05-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('momo', '0005_auto_20190514_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermatchmoney',
            name='win',
            field=models.IntegerField(default=0),
        ),
    ]
