# Generated by Django 5.0.6 on 2024-06-23 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_address_near_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]