# Generated by Django 4.2.7 on 2025-03-14 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_customuser_device_token_customuser_role_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='common_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('id1', models.CharField(max_length=255)),
            ],
        ),
    ]
