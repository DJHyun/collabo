# Generated by Django 2.1.8 on 2019-05-15 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('momo', '0003_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='movie',
        ),
        migrations.AddField(
            model_name='score',
            name='match',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='momo.Match'),
            preserve_default=False,
        ),
    ]
