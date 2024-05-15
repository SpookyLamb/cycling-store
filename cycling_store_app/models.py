from django.db import models

# Create your models here.

# =====================================

# Minimum Models Required

# Vehicle
# ○ type: unicycle, bicycle, tricycle
# ○ number_in_stock

# Customer
# ○ name

# CustomerOrder
# ○ customer
# ○ order: list of Vehicles ordered
# ○ created_date
# ○ paid: (boolean)

# =====================================

class Vehicle(models.Model):
    type = models.CharField(max_length=10)
    number_in_stock = models.IntegerField()

    def __str__(self) -> str:
        return f"VEHICLE | TYPE: {self.type} - STOCK: {self.number_in_stock}"

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"CUSTOMER | NAME: {self.name}"

class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ManyToManyField(Vehicle)
    created_date = models.DateTimeField()
    paid = models.BooleanField()

    def __str__(self) -> str:
        return f"ORDER | FROM: ({self.customer}) - ORDERED: ({self.order}) - CREATED ON: {self.created_date} - PAID?: {self.paid}"
