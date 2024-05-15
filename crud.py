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

def create_order(the_customer: Customer, ordered_vehicles: list, date_created: datetime.date, been_paid: bool):
    cust_order = CustomerOrder(customer=the_customer, created_date=date_created, paid=been_paid)
    cust_order.save()
    
    cust_order.order.set(ordered_vehicles)


# READ


def customers_by_name(cust_name: str):
    #prints a list of customers by name
    customers = Customer.objects.filter(name=cust_name)
    for customer in customers:
        print(customer)

def get_vehicle(vehicle_id: int, name: str = ""):

    if name: #grab vehicle by name, not id
        vehicle = Vehicle.objects.filter(type=name).first()
    else: #grab vehicle by id
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()

    return vehicle

def get_customer(cust_id: int) -> Customer:
    #gets a customer by ID ONLY, use customers_by_name() to grab a readout and find the ID
    return Customer.objects.get(id=cust_id)

def get_order(order_id: int):
    #gets an order by ID ONLY
    return CustomerOrder.objects.get(id=order_id)

def print_all():
    print_db(True, True, True)

def print_db(print_vehicles: bool, print_customers: bool, print_orders: bool):
    vehicles = Vehicle.objects.all()
    customers = Customer.objects.all()
    orders = CustomerOrder.objects.all()

    if print_vehicles:
        for vehicle in vehicles:
            print(vehicle)
    if print_customers:
        for customer in customers:
            print(customer)
    if print_orders:
        for order in orders:
            print(order)
            print("***")
            for vehicle in order.order.all():
                print(vehicle)
            print("***")


# UPDATE


def update():
    pass


# DELETE


def delete():
    pass
