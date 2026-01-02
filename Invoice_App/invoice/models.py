# invoices/models.py
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from company.models import Company


def validate_uae_mobile(value):
    number = str(value)
    if not number.startswith('+9715'):
        raise ValidationError("Enter a valid UAE mobile number")


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,
    blank=True)
    customer_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(
    region='AE',
    blank=True,
    null=True,
    validators=[validate_uae_mobile]
)
    service_description = models.TextField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    discount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    # this percentage will not save in database, IN UAE 5% VAT is fixed.
    VAT_PERCENTAGE = 5    

    def __str__(self):
        return f"Invoice {self.id} for {self.customer_name}"
    
    @property
    def subtotal(self):
        return max(self.amount_due - self.discount,0)
    
    @property
    def vat_amount(self):
        return (self.subtotal * self.VAT_PERCENTAGE) / 100

    # 🔹 Final total
    @property
    def total_amount(self):
        return self.subtotal + self.vat_amount
