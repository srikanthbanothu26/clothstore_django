# Generated by Django 5.0.6 on 2024-06-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_address_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='near_address',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
