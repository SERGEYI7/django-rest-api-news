# Generated by Django 4.0 on 2022-01-11 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='date',
            field=models.DateTimeField(blank=True, default='2022-01-12 03:46:12.526553', null=True),
        ),
    ]