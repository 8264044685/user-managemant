from django.db import models
from django.conf import settings
from .validation import validate_content
from djongo.models import ArrayModelField
from django.contrib.auth.models import User
from django.utils import timezone
from djongo import models
from datetime import datetime


# Create your models here.

#

class like(models.Model):
    comment_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class comment(models.Model):
    def ids():
        no = comment.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    comment_id = models.IntegerField(default=ids, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    messages = models.CharField(max_length=140, blank=True)
    time = models.DateTimeField(auto_now=True)
    no_of_like = models.IntegerField(blank=True)
    likes = ArrayModelField(model_container=like, null=True, blank=True)

    def __str__(self):
        return self.messages


class post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    content = models.CharField(max_length=140, validators=[validate_content], blank=True)
    updated = models.DateTimeField(default=datetime.now, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    comments = ArrayModelField(model_container=comment, null=True, blank=True)

    def __str__(self):
        return self.user.username
