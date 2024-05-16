import os
import django
from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "cycling_store.settings"
django.setup()

# DO NOT CHANGE CODE ABOVE THIS LINE
# WORK BELOW

import datetime
from cycling_store_app.models import *


# CREATE ********************************


def create_vehicle(type_name: str, in_stock: int, price: float, color: str):
    vehicle = Vehicle(type=type_name, number_in_stock=in_stock, price=price, color=color)
    vehicle.save()

def create_customer(cust_name: str):
    customer = Customer(name=cust_name)
    customer.save()

def create_order(the_customer: Customer, ordered_vehicles: list, been_paid: bool = False):
    date_created = datetime.date.today()
    cust_order = CustomerOrder(customer=the_customer, created_date=date_created, paid=been_paid)
    cust_order.save()
    
    cust_order.order.set(ordered_vehicles)

    return cust_order


# READ ********************************


def customers_by_name(cust_name: str):
    #prints a list of customers by name
    customers = Customer.objects.filter(name=cust_name)
    for customer in customers:
        print(customer)

def vehicle_by_name(name: str = ""):
    #grab vehicle by name, not id
    vehicle = Vehicle.objects.filter(type=name).first()
    print(vehicle)
    return vehicle.id

def get_vehicle(vehicle_id: int):
    #grab vehicle by ID ONLY, use vehicle_by_name to grab a readout and find the ID
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
    return vehicle

def get_customer(cust_id: int) -> Customer:
    #gets a customer by ID ONLY, use customers_by_name() to see a readout and grab the ID
    return Customer.objects.get(id=cust_id)

def get_order(order_id: int):
    #gets an order by ID ONLY
    return CustomerOrder.objects.get(id=order_id)

def print_all():
    print_db(True, True, True)

def print_db(print_vehicles: bool = False, print_customers: bool = False, print_orders: bool = False):
    vehicles = Vehicle.objects.all()
    customers = Customer.objects.all()
    orders = CustomerOrder.objects.all()

    if print_vehicles:
        for vehicle in vehicles:
            print(vehicle)
        print("")
    if print_customers:
        for customer in customers:
            print(customer)
        print("")
    if print_orders:
        for order in orders:
            print(order)
            print("***")
            for vehicle in order.order.all():
                print(vehicle)
            print("***")
        print("")    


# UPDATE ****************************************


def adjust_inventory(vehicle_id: int, adjustment: int):
    vehicle = get_vehicle(vehicle_id)
    stock = vehicle.number_in_stock
    stock += adjustment

    update_vehicle(vehicle_id, stock)

def update_vehicle(vehicle_id: int, in_stock: int, price: float = 0.0, color: str = "", name: str = ""):
    #updates a vehicle BY ID
    vehicle = get_vehicle(vehicle_id)
    vehicle.number_in_stock = in_stock

    if name:
        vehicle.type = name
    if price > 0:
        vehicle.price = price
    if color:
        vehicle.color = color

    vehicle.save()

def update_customer(cust_id: int, update_name: str):
    #updates a customer BY ID
    customer = get_customer(cust_id)
    
    if update_name:
        customer.name = update_name
    customer.save()

def update_order(order_id: int, order_list: list, has_paid: bool):
    #updates a customer's order BY ID
    #can't change WHO ordered something, that'd be stupid!
    #can change what they ordered, though
    #updates the created date to the CURRENT DAY automatically

    order = get_order(order_id)
    
    order.created_date = datetime.date.today()
    order.paid = has_paid
    order.save()

    if len(order_list) > 0:
        order.order.set(order_list)


# DELETE ************************************


def delete_all(): #TABULA RASA
    #dangerous!!
    vehicles = Vehicle.objects.all()
    customers = Customer.objects.all()
    orders = CustomerOrder.objects.all()

    user_input = input("Are you SURE you want to delete the entire database? ").upper()
     
    if user_input == "Y" or user_input == "YES":
        for vehicle in vehicles:
            vehicle.delete()
        for customer in customers:
            customer.delete()
        for order in orders:
            order.delete()
    else:
        print("Phew!")
        return

def delete_vehicle(vehicle_id: int):
    vehicle = get_vehicle(vehicle_id)
    vehicle.delete()

def delete_customer(customer_id: int):
    customer = get_customer(customer_id)
    customer.delete()

def delete_order(order_id: int):
    order = get_order(order_id)
    order.delete()
