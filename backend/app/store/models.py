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

	most_sales  = models.ForeignKey(
		'Product', on_delete=models.DO_NOTHING, related_name='+'
		)

	genre       = models.CharField(max_length=255)
	about       = models.CharField(max_length=255, blank=True)

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
		Category, on_delete=models.PROTECT, related_name='products'
		)
	
    discounts     = models.ManyToManyField(
		Discount, blank=True, related_name='products'
		)
	
    name          = models.CharField(max_length=255)
    slug          = models.SlugField(unique=True)
    description   = models.TextField()
    unit_price    = models.DecimalField(max_digits=6, decimal_places=2)
    inventory     = models.PositiveIntegerField()
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.name


class Order(models.Model):
	"""
	FOR AUTHENTICATED USERS
	"""
	ORDER_STATUS_PAID     = 'P'
	ORDER_STATUS_UNPAID   = 'U'
	ORDER_STATUS_CANCELED = 'C'

	ORDER_STATUS_CHOICES = (
		(ORDER_STATUS_PAID,         'Paid'),
		(ORDER_STATUS_UNPAID,     'Unpaid'),
		(ORDER_STATUS_CANCELED, 'Canceled'),
	)

	customer = models.ForeignKey(
		Customer, on_delete=models.PROTECT, related_name='orders'
		)
	
	datetime_created = models.DateTimeField(auto_now_add=True)
	status           = models.CharField(
		                                max_length=1,
										choices=ORDER_STATUS_CHOICES, 
										default=ORDER_STATUS_UNPAID
										)

	def __str__(self):
		return F"{self.__class__.__name__}={self.id}"


class OrderItem(models.Model):

	product        = models.ForeignKey(
                            Product, on_delete=models.PROTECT, related_name='order_items'
                                        )
	
	product_amount = models.ForeignKey(
                            Order, on_delete=models.PROTECT, related_name='items'
                                    )

	quantity       = models.PositiveSmallIntegerField()
	unit_price     = models.DecimalField(max_digits=6, decimal_places=2)

	class Meta:
		unique_together = [['product', 'product_amount']]

	def __str__(self):
		return self.product.name


class TempCart(models.Model):
    """
	TEMPORARY CART FOR ANON USERS
	"""

    id               = models.UUIDField(primary_key=True, default=uuid4)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
    	db_table = 'temporary_cart'

class TempCartItem(models.Model):

	cart     = models.ForeignKey(
		TempCart, on_delete=models.CASCADE, related_name='items'
		)
	
	items  = models.ForeignKey(
		Product, on_delete=models.CASCADE, related_name='cart_items'
		)

	quantity = models.PositiveSmallIntegerField()


	class Meta:
		db_table        = 'cartitems'
		unique_together = [['cart', 'items']]


