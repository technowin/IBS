# Generated by Django 4.2.7 on 2025-03-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application_search',
            name='extra',
            field=models.TextField(blank=True, null=True),
        ),
    ]
