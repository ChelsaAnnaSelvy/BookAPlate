# Generated by Django 4.2.1 on 2023-12-26 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0009_alter_bookingdetails_booked_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
