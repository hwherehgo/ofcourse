from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    createtime = models.DateTimeField(auto_now_add=True)


