from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        ('M','男'),('N','女'),('U','保密')
    )
    nickname = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    sex = models.CharField(max_length=8,choices=SEX)
    age = models.IntegerField()