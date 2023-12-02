# Generated by Django 4.2.1 on 2023-11-23 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0006_facilitydetails_floor_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitydetails',
            name='floor_number',
            field=models.CharField(choices=[('First Floor', 'First Floor'), ('Second Floor', 'Second Floor'), ('Third Floor', 'Third Floor'), ('Fourth Floor', 'Fourth Floor'), ('Top Floor', 'Top Floor')], default='First Floor', max_length=100),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='seat_arrangement',
            field=models.CharField(choices=[('Outdoor', 'Outdoor'), ('Indoor', 'Indoor')], default='Indoor', max_length=100),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='seat_count',
            field=models.IntegerField(default=2),
        ),
    ]
