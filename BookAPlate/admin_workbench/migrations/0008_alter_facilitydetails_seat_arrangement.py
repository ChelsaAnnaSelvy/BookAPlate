# Generated by Django 4.2.1 on 2023-12-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0007_remove_restaurant_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitydetails',
            name='seat_arrangement',
            field=models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor')], default='Indoor', max_length=100, null=True),
        ),
    ]