# Generated by Django 3.2.7 on 2024-03-07 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_login_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Dob',
            field=models.CharField(max_length=200),
        ),
    ]
