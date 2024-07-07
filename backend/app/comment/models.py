from django.db import models

from ..store.models import Product


#TODO add user after auth process completed
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