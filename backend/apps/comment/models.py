from django.conf import settings
from django.db import models

from ..store.models import Product


class Comment(models.Model):
    commentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    COMMENT_STATUS_WAITING = "W"
    COMMENT_STATUS_APPROVED = "A"
    COMMENT_STATUS_NOT_APPROVED = "N"

    COMMENT_STATUS_CHOICES = (
        (COMMENT_STATUS_WAITING, "WAITING"),
        (COMMENT_STATUS_APPROVED, "APPROVED"),
        (COMMENT_STATUS_NOT_APPROVED, "NOT APPROVED"),
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )

    content = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_WAITING
    )  # get_status_display()

    def __str__(self):
        return self.content
