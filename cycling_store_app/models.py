from django.db import models

# Create your models here.

# =====================================

# Minimum Models Required

# Vehicle
# ○ type: unicycle, bicycle, tricycle
# ○ number_in_stock
# ○ price
# ○ color

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
    price = models.FloatField(default=1.0)
    color = models.CharField(max_length=15, default="black")

    def __str__(self) -> str:
        return f"VEHICLE | ID: {self.id} - TYPE: {self.type} - STOCK: {self.number_in_stock} - PRICE: {self.price} - COLOR: {self.color}"

class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"CUSTOMER | NAME: {self.name} - ID: {self.id}"

class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ManyToManyField(Vehicle)
    created_date = models.DateField()
    paid = models.BooleanField()

    def __str__(self) -> str:
        return f"ORDER | ID: {self.id} | FROM: ({self.customer}) - CREATED ON: {self.created_date} - PAID?: {self.paid}"
