# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Suburb(models.Model):
    id = models.TextField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    postcode = models.TextField(db_column='Postcode')  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude')  # Field name made lowercase.
    averagerent_in_2013 = models.IntegerField(db_column='Averagerent in 2013')  # Field name made lowercase. Field renamed to remove unsuitable characters.
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


class SuburbUniversity(models.Model):
    suburb_name = models.TextField(db_column='Suburb_name', unique=True)  # Field name made lowercase.
    university_name = models.TextField(db_column='University_name', primary_key=True)  # Field name made lowercase.
    distance = models.TextField(db_column='Distance', unique=True, blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Suburb_university'


class University(models.Model):
    id = models.TextField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    suburbname = models.TextField(db_column='Suburbname')  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude')  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'University'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
