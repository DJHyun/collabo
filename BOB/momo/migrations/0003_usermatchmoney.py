# Generated by Django 2.1.8 on 2019-05-14 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('momo', '0002_auto_20190514_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMatchMoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updown', models.IntegerField(default=0)),
                ('point', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='momo.Match')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
