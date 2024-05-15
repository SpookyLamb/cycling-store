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

def main_menu():

    while True:

        print("")
        print("***********")
        print(" MAIN MENU ")
        print("***********")
        print("")

        print("OPTIONS: ")
        print("display-inventory")
        print("view-customers")
        print("view-all-orders")
        print("order-vehicles [VEHICLE ID] [AMOUNT TO ORDER]")
        print("create-customer [CUSTOMER NAME]")
        print("create-order [CUSTOMER ID] [VEHICLE ID]")
        print("cancel-order [ORDER ID]")
        print("mark-order-paid [ORDER ID]")
        print("help")
        print("quit")
        print("")

        user_input = input("What would you like to do today? ")
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

            elif user_input.startswith("order-vehicles"):
                vehicle_id = int(array[1])
                amount = int(array[2])
                adjust_inventory(vehicle_id, amount)
                print("Ordered inventory!")
            
            elif user_input.startswith("create-customer"):
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
            
            elif user_input.startswith("cancel-order"):
                order_id = int(array[1])
                order = get_order(order_id)

                #return to inventory
                for vehicle in order.order.all():
                    vehicle_id = vehicle.id
                    adjust_inventory(vehicle_id, 1)

                delete_order(order_id)
                print("Cancelled and deleted order!")
            
            elif user_input.startswith("mark-order-paid"):
                order_id = int(array[1])
                update_order(order_id, [], True) #empty array means DON'T change the order
                print("Order marked as paid!")
            
            elif user_input == "help":
                pass
        except:
            input("ERROR! Bad input! Check your input and press enter when you're ready to try again!")
        
        if user_input == "quit":
            print("Quitting!")
            break

main_menu()