__author__ = 'evangelie'
from django.db import models
from django.contrib.auth.models import User

class UserCredentials(models.Model):
    id = models.AutoField(primary_key=True)
    #username = models.TextField(db_column='userName', blank=False)  # Field name made lowercase.
    user = models.ForeignKey(User,blank=False)
    #code = models.TextField(db_column='code')  # Field name made lowercase.
    credentials = models.TextField(db_column='credentials', blank=False)  # Field name made lowercase.
