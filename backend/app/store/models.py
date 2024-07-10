"""
STOR:
	CATEGORY FOR PRODUCTS,
	FINAL PRODUCTS,
	CUSTOMER ORDER CART => REAL CART, 
	TEMPORARY CART FOR ANON USERS => PSEUDO CART
	 
	[
	ORDER PROCESS:
		ANON USERS CAN ADD DELETE ITEM TO THEIR TEMPORARY CART,
		WHEN CHECKOUT, THEY HAVE TO LOGIN,
		THEN WE MAKE A CUSTOMER ORDER WITH DETAIL OF CUSTOMER
	]
"""

from django.db import models
from uuid import uuid4

from ..roles.models import Customer


class Category(models.Model):
	genre       = models.CharField(max_length=255, db_index=True)
	about       = models.CharField(max_length=255, blank=True, default="")

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.genre


class Discount(models.Model):
	discount    = models.FloatField()
	description = models.CharField(max_length=255)

	def __str__(self):
		return F"{str(self.discount)} | {self.description}"


class Product(models.Model):

    category      = models.ForeignKey(
									Category, 
									on_delete=models.PROTECT, 
									related_name='products', 
									db_index=True
									)
	
    discounts     = models.ManyToManyField(
										Discount, 
										blank=True, 
										related_name='products'
										)
	
    name          = models.CharField(max_length=255, db_index=True)
    slug          = models.SlugField(unique=True, db_index=True)
    description   = models.TextField()
    unit_price    = models.DecimalField(max_digits=6, decimal_places=2)
    inventory     = models.PositiveIntegerField()
    dt_created  = models.DateTimeField(auto_now_add=True)
    dt_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.name


class Order(models.Model):
	"""
	FOR AUTHENTICATED CUSTOMERS
	"""
	ORDER_STATUS_PAID     = 'P'
	ORDER_STATUS_UNPAID   = 'U'
	ORDER_STATUS_CANCELED = 'C'

	ORDER_STATUS_CHOICES = (
		(ORDER_STATUS_PAID,         'Paid'),
		(ORDER_STATUS_UNPAID,     'Unpaid'),
		(ORDER_STATUS_CANCELED, 'Canceled'),
	)

	customer 	= models.ForeignKey(
									Customer, 
									on_delete=models.PROTECT, 
									related_name='orders', 
									db_index=True
									)
	
	dt_created  = models.DateTimeField(auto_now_add=True)
	status      = models.CharField(
									max_length=1,
									choices=ORDER_STATUS_CHOICES, 
									default=ORDER_STATUS_UNPAID
									)

	def __str__(self):
		return F"{self.__class__.__name__}={self.id}"


class OrderItem(models.Model):

	product     	= models.ForeignKey(
										Product, 
										on_delete=models.PROTECT, related_name='order_items',
										db_index=True
										)
			
	product_amount  = models.ForeignKey(
										Order, 
										on_delete=models.PROTECT, 
										related_name='items'
										)

	quantity        = models.PositiveSmallIntegerField()
	unit_price      = models.DecimalField(max_digits=6, decimal_places=2)

	class Meta:
		unique_together = [['product', 'product_amount']]

	def __str__(self):
		return self.product.name


class Cart(models.Model):
	"""
	TEMPORARY CART FOR ANON USERS
	"""
	id          = models.UUIDField(
									primary_key=True, 
									default=uuid4
									)
	dt_created  = models.DateTimeField(auto_now_add=True)	
	
	class Meta:
		db_table = 'temporary_cart'
		verbose_name_plural = 'carts'

class CartItem(models.Model):

	cart        = models.ForeignKey(
									Cart, 
									on_delete=models.CASCADE, 
									related_name='items'
									)
	
	product  		= models.ForeignKey(
									Product, 
									on_delete=models.CASCADE, 
									related_name='cart_items'
									)

	quantity    = models.PositiveSmallIntegerField()

	class Meta:
		db_table        = 'cartitem'
		unique_together = [['cart', 'product']]


