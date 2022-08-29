from operator import mod
from django.db import models
# class Suburb(models.Model):

# Create your models here.

from django.db import models
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    age = models.IntegerField()

class University(models.Model):
    name = models.TextField(db_column='Name', primary_key=True)  # Field name made lowercase.
    suburbname = models.TextField(db_column='Suburbname')  # Field name made lowercase.
    location = models.TextField(db_column='Location', unique=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'University'

class Suburb(models.Model):
    name = models.TextField(db_column='Name', primary_key=True)  # Field name made lowercase.
    postcode = models.IntegerField(db_column='Postcode')  # Field name made lowercase.
    crime_rate = models.IntegerField(db_column='Crime rate')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    average_rent = models.IntegerField(db_column='Average rent')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    location = models.TextField(db_column='Location')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Suburb'