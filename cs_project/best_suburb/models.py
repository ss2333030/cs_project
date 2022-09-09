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
    latitude = models.TextField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    longitude = models.TextField(db_column='Longitude')  # Field name made lowercase. This field type is a guess.
    averagerent_in_2013 = models.TextField(db_column='Averagerent in 2013')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2014 = models.IntegerField(db_column='Averagerent in 2014')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2015 = models.IntegerField(db_column='Averagerent in 2015')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2016 = models.IntegerField(db_column='Averagerent in 2016')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2017 = models.IntegerField(db_column='Averagerent in 2017')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2018 = models.IntegerField(db_column='Averagerent in 2018')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2019 = models.IntegerField(db_column='Averagerent in 2019')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2020 = models.IntegerField(db_column='Averagerent in 2020')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2021 = models.IntegerField(db_column='Averagerent in 2021')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    averagerent_in_2022 = models.IntegerField(db_column='Averagerent in 2022')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2013 = models.IntegerField(db_column='Crime rate in 2013')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2014 = models.IntegerField(db_column='Crime rate in 2014')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2015 = models.IntegerField(db_column='Crime rate in 2015')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2016 = models.IntegerField(db_column='Crime rate in 2016')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2017 = models.IntegerField(db_column='Crime rate in 2017')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2018 = models.IntegerField(db_column='Crime rate in 2018')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2019 = models.IntegerField(db_column='Crime rate in 2019')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2020 = models.IntegerField(db_column='Crime rate in 2020')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2021 = models.IntegerField(db_column='Crime rate in 2021')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    crime_rate_in_2022 = models.IntegerField(db_column='Crime rate in 2022')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Suburb'