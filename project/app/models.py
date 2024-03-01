from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Crypto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_data')
    asset_name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_purchased = models.DecimalField(max_digits=10, decimal_places=5)
    
    @property
    def total_dollar_amount(self):
        return self.purchase_price * self.quantity_purchased
    
    def __str__(self):
        return f"{self.user.username} - {self.asset_name}"