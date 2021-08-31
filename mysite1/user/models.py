from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=32)
    desc = models.TextField(default=' ')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user'

    pass


class Note(models.Model):
    title = models.CharField(max_length=50, default='title')
    content = models.TextField()
    create_date = models.DateTimeField('create time', auto_now_add=True)
    mod_date = models.DateTimeField('last time', auto_now=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'note'

    pass


class Kind(models.Model):
    name = models.CharField(max_length=10, default='', unique=True)
    notes = models.ManyToManyField(to='Note')

    class Meta:
        db_table = 'kind'


class UploadFile(models.Model):
    info = models.CharField(max_length=11)
    file_path = models.FileField(upload_to='picture')
    user = models.ForeignKey(to='user', on_delete=models.CASCADE)
