# Generated by Django 3.2.5 on 2021-07-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='modalidade',
            field=models.CharField(choices=[('renda fixa', 'renda fixa'), ('renda variável', 'renda variável'), ('cripto', 'cripto')], max_length=14),
        ),
    ]