from django.db import models
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission, User

class Trial(models.Model):

	title = models.CharField(max_length=100)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=20)
	country = models.CharField(max_length=20)
	pincode = models.IntegerField()
	discription = models.CharField(max_length=200)
	email = models.EmailField()
	operator =models.CharField(max_length=100)
	organiser =models.CharField(max_length=100)

class Enrollment(models.Model):
    patient_username = models.CharField(max_length=100)
    email = models.EmailField()
    trial_title = models.CharField(max_length=100)
    trial_organiser = models.CharField(max_length=100)
    trial_operator = models.CharField(max_length=100)