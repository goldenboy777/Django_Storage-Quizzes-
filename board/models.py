
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
# Create your models here.

def UploadedConfigPath(instance, filename):
    return os.path.join('documents', str(instance.subject.board),str(instance.subject), filename)

class User(AbstractUser):
	is_student=models.BooleanField(default=False)
	is_moderator=models.BooleanField(default=False)


class Board(models.Model):
    name=models.CharField(max_length=30,unique=True)
   
    def __str__(self):
        return self.name


class Subject(models.Model):
    name=models.CharField(max_length=30,unique=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE,related_name='subjects')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='subjects')

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   
    def __str__(self):
        return self.user.username

class Document(models.Model):
    name = models.CharField(max_length=255,unique=True)
    document = models.FileField(upload_to=UploadedConfigPath)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)	
    uploaded_by=models.ForeignKey(Student,on_delete=models.CASCADE ,related_name='documents')
    is_reviewed=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    