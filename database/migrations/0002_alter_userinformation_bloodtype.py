# Generated by Django 5.0.6 on 2024-06-18 20:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='bloodType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.bloodtype'),
        ),
    ]
