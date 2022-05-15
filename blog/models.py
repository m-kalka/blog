from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.timezone import now


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=now ,editable=False)

    

    def __str__(self):
        return f"{self.user}: {self.title}"

admin.site.register(Post)