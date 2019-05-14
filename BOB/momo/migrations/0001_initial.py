# Generated by Django 2.1.8 on 2019-05-14 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('poster_url', models.ImageField(blank=True, upload_to='')),
                ('audiCnt', models.IntegerField()),
                ('audinten', models.IntegerField()),
                ('audiChange', models.FloatField()),
                ('auidAcc', models.IntegerField()),
                ('userRating', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='momo.Movie'),
        ),
        migrations.AddField(
            model_name='match',
            name='user_down',
            field=models.ManyToManyField(blank=True, related_name='down', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='user_up',
            field=models.ManyToManyField(blank=True, related_name='up', to=settings.AUTH_USER_MODEL),
        ),
    ]
