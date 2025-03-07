# Generated by Django 4.2.7 on 2025-03-07 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='device_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='superior_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
