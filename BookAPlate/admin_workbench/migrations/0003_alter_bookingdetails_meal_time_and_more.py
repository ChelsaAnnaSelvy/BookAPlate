# Generated by Django 4.2.1 on 2023-11-23 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0002_alter_bookingdetails_meal_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetails',
            name='meal_time',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Supper', 'Supper'), ('Full Day', 'Full Day')], default='Choose Meal Time', max_length=100),
        ),
        migrations.AlterField(
            model_name='bookingdetails',
            name='slot_requested',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookingdetails',
            name='status',
            field=models.CharField(choices=[('Requested', 'Requested'), ('Completed', 'Completed'), ('Cancelled', 'Cacelled')], default='Requested', max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal')], default='Kerala', max_length=100),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='facility_name',
            field=models.CharField(choices=[('Table', 'Table'), ('Banquet Hall', 'Banquet Hall'), ('Conference Hall', 'Conference Hall')], default='Choose Facility', max_length=100),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='facility_number',
            field=models.CharField(default='Facility Number', max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='position',
            field=models.CharField(choices=[('Top', 'Top'), ('Bottom', 'Bottom'), ('Left', 'Left'), ('Right', 'Right'), ('Center', 'Center')], default='Select Position', max_length=100),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='seat_arrangement',
            field=models.CharField(choices=[('Outdoor', 'Outdoor'), ('Indoor', 'Indoor'), ('First Floor', 'First Floor'), ('Second Floor', 'Second Floor'), ('Third Floor', 'Third Floor'), ('Fourth Floor', 'Fourth Floor'), ('Top Floor', 'Top Floor')], default='Select Seating Location', max_length=100),
        ),
        migrations.AlterField(
            model_name='facilitydetails',
            name='seat_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='category',
            field=models.CharField(choices=[('Menu', 'Menu'), ('Gallery', 'Gallery')], default='Gallery', max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='state',
            field=models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal')], default='Kerala', max_length=100),
        ),
    ]
