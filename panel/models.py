from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, default="", blank=True)
    category = models.CharField(max_length=50, default="", blank=True)
    date_release = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)

    def __str__(self):
        return self.name


class ProductPriceChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.CharField(max_length=50, default="", blank=True)
    new_price = models.CharField(max_length=50, default="", blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
