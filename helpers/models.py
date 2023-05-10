from django.db import models
from django.core.validators import MinValueValidator


class TrakingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class DishListRoot(TrakingModel):

    dish_name = models.CharField(max_length=255)
    dish_id = models.CharField(max_length=255, null=False, blank=False)
    dish_quantity = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)])

    class Meta:
        abstract = True
        ordering = ('-created_at',)
