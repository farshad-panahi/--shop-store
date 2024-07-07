"""
AUTHENTICATION, PROFILE MANAGEMENT
"""


from django.conf import settings
from django.db import models


class Customer(models.Model):
	
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL, on_delete=models.PROTECT
		)

	phone = models.CharField(max_length=11)
	birth_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name


class Address(models.Model):
	
	customer = models.OneToOneField(
		Customer, on_delete=models.CASCADE, primary_key=True
		)
	
	province = models.CharField(max_length=255)
	city     = models.CharField(max_length=255)
	street   = models.CharField(max_length=255)
    
	def __str__(self):
		return self.province
	
	class Meta:
		db_table = 'customer_address'

