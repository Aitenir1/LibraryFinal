# Generated by Django 4.2 on 2023-04-05 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_book_author_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, default='image1.jpeg', null=True, upload_to=''),
        ),
    ]
