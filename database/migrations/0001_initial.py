# Generated by Django 5.0.6 on 2024-06-18 20:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bloodtype', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Govern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_donation', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GovernStates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('govername', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.govern')),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=11)),
                ('govern', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('Card_number', models.CharField(max_length=14)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20)),
                ('bloodType', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.bloodtype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]