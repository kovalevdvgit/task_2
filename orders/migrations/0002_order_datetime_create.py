# Generated by Django 4.2.5 on 2023-09-29 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='datetime_create',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
