import os
import django
from django.conf import settings
# Use this by running:
# python standalone_script.py
os.environ["DJANGO_SETTINGS_MODULE"] = "cycling_store.settings"
django.setup()

import datetime
from cycling_store_app.models import *
from crud import *

def exception():
    input("ERROR! Bad input! Check your input and press enter when you're ready to try again!")

def create_menu():

    while True:

        print("")
        print("*****************")
        print(" DATABASE CREATE ")
        print("*****************")
        print("")

        print("OPTIONS: ")
        print("create-customer [CUSTOMER NAME]")
        print("create-order [CUSTOMER ID] [VEHICLE ID]")
        print("back")
        print("")

        user_input = input("What would you like to create today? ")
        user_input = user_input.strip()
        array = user_input.split(" ")

        try:
            if user_input.startswith("create-customer"):
                name = array[1]
                create_customer(name)
                print("Created customer!")
            
            elif user_input.startswith("create-order"):
                customer_id = int(array[1])
                vehicle_id = int(array[2])

                customer = get_customer(customer_id)
                vehicle = get_vehicle(vehicle_id)

                create_order(customer, [vehicle], False)
                adjust_inventory(vehicle_id, -1)
                print("Created order!")

            elif user_input == "back":
                print("Going back!")
                break

            else:
                exception()
        except:
            exception()

def read_menu():
    
    while True:
        print("")
        print("***************")
        print(" DATABASE READ ")
        print("***************")
        print("")

        print("OPTIONS: ")
        print("display-inventory")
        print("view-customers")
        print("view-all-orders")
        print("back")
        print("")

        user_input = input("What would you like to read today? ")
        user_input = user_input.strip()
        array = user_input.split(" ")

        try:
            if user_input == "display-inventory":
                print_db(True)
                input("Press enter to continue...")
            
            elif user_input == "view-customers":
                print_db(False, True)
                input("Press enter to continue...")
            
            elif user_input == "view-all-orders":
                print_db(False, False, True)
                input("Press enter to continue...")
            
            elif user_input == "back":
                print("Going back!")
                break

            else:
                exception()
        except:
            exception()


def update_menu():

    while True:

        print("")
        print("*****************")
        print(" DATABASE UPDATE ")
        print("*****************")
        print("")

        print("OPTIONS: ")
        print("order-vehicles [VEHICLE ID] [AMOUNT TO ORDER]")
        print("mark-order-paid [ORDER ID]")
        print("back")
        print("")

        user_input = input("What would you like to update today? ")
        user_input = user_input.strip()
        array = user_input.split(" ")

        try:
            if user_input.startswith("order-vehicles"):
                vehicle_id = int(array[1])
                amount = int(array[2])
                adjust_inventory(vehicle_id, amount)
                print("Ordered inventory!")
            
            elif user_input.startswith("mark-order-paid"):
                order_id = int(array[1])
                update_order(order_id, [], True) #empty array means DON'T change the order
                print("Order marked as paid!")
            
            elif user_input == "back":
                print("Going back!")
                break

            else:
                exception()
        except:
            exception()

def delete_menu():
    
    while True:

        print("")
        print("*****************")
        print(" DATABASE DELETE ")
        print("*****************")
        print("")

        print("OPTIONS: ")
        print("cancel-order [ORDER ID]")
        print("back")
        print("")

        user_input = input("What would you like to delete today? ")
        user_input = user_input.strip()
        array = user_input.split(" ")

        try:
            if user_input.startswith("cancel-order"):
                order_id = int(array[1])
                order = get_order(order_id)

                #return to inventory
                for vehicle in order.order.all():
                    vehicle_id = vehicle.id
                    adjust_inventory(vehicle_id, 1)

                delete_order(order_id)
                print("Cancelled and deleted order!")

            elif user_input == "back":
                print("Going back!")
                break

            else:
                exception()
        except:
            exception()

def main_menu():

    while True:

        print("")
        print("***********")
        print(" MAIN MENU ")
        print("***********")
        print("")

        print("OPTIONS: ")
        print("create")
        print("read")
        print("update")
        print("delete")
        print("help")
        print("quit")
        print("")

        user_input = input("What would you like to do today? ")
        user_input = user_input.strip()
        array = user_input.split(" ")

        try:

            if user_input == "create":
                create_menu()
            
            elif user_input == "read":
                read_menu()
            
            elif user_input == "update":
                update_menu()
            
            elif user_input == "delete":
                delete_menu()
            
            elif user_input == "help":
                pass

            elif user_input == "quit":
                print("Quitting!")
                break

            else:
                exception()
        except:
            exception()

main_menu()