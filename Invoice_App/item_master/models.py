from django.db import models

# Create your models here.
class new_item(models.Model):
    tyre=models.CharField(max_length=50)
    tube=models.CharField(max_length=50)
    tyre_valve=models.CharField(max_length=50)
    date_created=models.DateField(auto_now_add=True)
    stock_quantity = models.IntegerField(default=0)


    def __str__(self):
        return f"Inventory Item: {self.tyre} - {self.tube} - {self.tyre_valve}"
