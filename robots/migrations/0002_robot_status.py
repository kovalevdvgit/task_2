# Generated by Django 4.2.5 on 2023-10-01 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='status',
            field=models.CharField(choices=[('g', 'Готов к выдаче'), ('p', 'Передан в упаковочный цех')], default='g', max_length=1),
        ),
    ]
