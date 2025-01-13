from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    json_db = models.FileField()
    json_db_id = models.CharField(max_length=1000)

class Etude(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    thread_id = models.CharField(max_length=1000)
    vs_id = models.CharField(max_length=1000)

# Create your models here.
