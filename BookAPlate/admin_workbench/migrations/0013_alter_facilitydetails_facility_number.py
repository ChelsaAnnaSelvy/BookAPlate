# Generated by Django 4.2.1 on 2023-12-03 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0012_remove_bookingdetails_slot_requested_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitydetails',
            name='facility_number',
            field=models.CharField(max_length=10),
        ),
    ]