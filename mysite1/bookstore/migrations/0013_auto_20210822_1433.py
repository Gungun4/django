# Generated by Django 2.2.12 on 2021-08-22 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0012_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
