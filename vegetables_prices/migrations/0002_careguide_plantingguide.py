# Generated by Django 5.1.4 on 2024-12-13 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vegetables_prices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('vegetable', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vegetables_prices.vegetable')),
            ],
        ),
        migrations.CreateModel(
            name='PlantingGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('vegetable', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vegetables_prices.vegetable')),
            ],
        ),
    ]
