import os
import django
from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "cycling_store.settings"
django.setup()

# DO NOT CHANGE CODE ABOVE THIS LINE
# WORK BELOW

import datetime
from cycling_store_app.models import *

# CREATE

def create_vehicle(type_name: str, in_stock: int):
    vehicle = Vehicle(type=type_name, number_in_stock=in_stock)
    vehicle.save()

def create_customer(cust_name: str):
    customer = Customer(name=cust_name)
    customer.save()

def create_order(the_customer: Customer, ordered_vehicles: list, date_created: datetime, been_paid: bool):
    order = CustomerOrder(customer=the_customer, order=ordered_vehicles, created_date=date_created, paid=been_paid)
    order.save()

# READ

def print_all():
    print_db(True, True, True)

def print_db(print_vehicles, print_customers, print_orders):
    vehicles = Vehicle().objects.all()
    customers = Customer().objects.all()
    orders = CustomerOrder().objects.all()

    if print_vehicles:
        for vehicle in vehicles:
            print(vehicle)
    if print_customers:
        for customer in customers:
            print(customer)
    if print_orders:
        for order in orders:
            print(order)

# UPDATE

def update():
    pass

# DELETE

def delete():
    pass