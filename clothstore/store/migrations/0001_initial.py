# Generated by Django 5.0.6 on 2024-06-13 08:50

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
            name='Shirt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='shirt_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discountPrice', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('Oversized', 'Oversized'), ('Regular', 'Regular'), ('Slim Fit', 'Slim Fit'), ('Classic', 'Classic'), ('Dropcut', 'Dropcut')], default='Regular', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ShirtSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Extra Extra Large')], max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('shirt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shirt_sizes', to='store.shirt')),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='store.shirt')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
