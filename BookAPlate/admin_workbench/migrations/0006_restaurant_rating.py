# Generated by Django 4.2.1 on 2023-12-14 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_workbench', '0005_alter_bookingdetails_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2, null=True),
        ),
    ]
