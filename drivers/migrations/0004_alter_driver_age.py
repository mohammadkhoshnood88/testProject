# Generated by Django 3.2.6 on 2021-08-10 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0003_alter_car_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='age',
            field=models.FloatField(default=20),
        ),
    ]
