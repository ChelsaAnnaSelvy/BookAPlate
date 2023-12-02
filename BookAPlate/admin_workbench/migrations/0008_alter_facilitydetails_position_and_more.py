# Generated by Django 4.2.1 on 2023-11-23 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0007_alter_facilitydetails_floor_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitydetails',
            name='position',
            field=models.CharField(choices=[('Top', 'Top'), ('Bottom', 'Bottom'), ('Left', 'Left'), ('Right', 'Right'), ('Center', 'Center')], default='Select Position', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='seat_arrangement',
            field=models.CharField(choices=[('Outdoor', 'Outdoor'), ('Indoor', 'Indoor')], default='Indoor', max_length=100, null=True),
        ),
    ]