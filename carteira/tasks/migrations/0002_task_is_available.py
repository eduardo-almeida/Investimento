# Generated by Django 3.2.5 on 2021-07-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]