# Generated by Django 4.2 on 2023-04-06 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_book_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrower',
            name='email',
        ),
        migrations.RemoveField(
            model_name='borrower',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='borrower',
            name='last_name',
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]