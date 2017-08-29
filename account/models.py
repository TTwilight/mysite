from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class ProfileUser(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    birth=models.DateField(blank=True,default='2017-01-01')
    come_from=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
    others=models.TextField(default='SOME STRING')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)