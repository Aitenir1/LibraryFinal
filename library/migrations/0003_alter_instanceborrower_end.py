# Generated by Django 4.2 on 2023-04-03 17:31

from django.db import migrations, models
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_borrower_debt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instanceborrower',
            name='end',
            field=models.DateTimeField(blank=True, default=library.models.get_time, null=True),
        ),
    ]
