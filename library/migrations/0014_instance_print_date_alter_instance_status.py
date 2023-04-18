# Generated by Django 4.2 on 2023-04-10 17:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_remove_instance_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='print_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instance',
            name='status',
            field=models.IntegerField(choices=[(0, 'False'), (1, 'True')], default=1),
        ),
    ]