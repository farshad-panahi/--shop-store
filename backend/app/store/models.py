"""

"""

from django.db import models
from uuid import uuid4
from django.conf import settings


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
		'Customer', on_delete=models.PROTECT, related_name='orders'
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

class Comment(models.Model):

    COMMENT_STATUS_WAITING      = 'W'
    COMMENT_STATUS_APPROVED     = 'A'
    COMMENT_STATUS_NOT_APPROVED = 'N'
    
    COMMENT_STATUS_CHOICES = (
		(COMMENT_STATUS_WAITING,           'WAITING'),
		(COMMENT_STATUS_APPROVED,         'APPROVED'),
		(COMMENT_STATUS_NOT_APPROVED, 'NOT APPROVED')
	)
    
    product = models.ForeignKey(
		Product, on_delete=models.CASCADE, related_name='comments'
		)
    
    name             = models.CharField(max_length=255)
    body             = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status           = models.CharField(
		                                max_length=1, 
		                                choices=COMMENT_STATUS_CHOICES, 
		                                default=COMMENT_STATUS_WAITING
										)

    def __str__(self):
    	return self.name