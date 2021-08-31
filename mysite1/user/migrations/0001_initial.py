# Generated by Django 2.2.12 on 2021-08-23 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=16, unique=True)),
                ('password', models.IntegerField(default=0, max_length=16)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='title', max_length=50)),
                ('text', models.CharField(default='', max_length=100)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='last time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'note',
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10, unique=True)),
                ('notes', models.ManyToManyField(to='user.Note')),
            ],
            options={
                'db_table': 'kind',
            },
        ),
    ]
