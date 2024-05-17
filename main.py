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

def process_list_input(user_input: str):
    array = []

    #need to find the left bracket, right bracket, and then grab everything between
    #we can then delete that from the original string and split it to get processable data
    left_index = user_input.find("[")
    right_index = user_input.rfind("]")
    list_string = ""

    for i in range(left_index + 1, right_index):
        list_string += user_input[i]
    
    user_input = user_input.replace("[" + list_string + "] ", "") #strip list from user input
    list_string = list_string.replace(",", "") #strip all commas from list
    order_list = list_string.split(" ") #grab a real list

    for i in range(len(order_list)):
        order_list[i] = int(order_list[i]) #convert all strings in this list to numbers
    
    array = user_input.split(" ") #get our elements
    array.append(order_list) #append list to create a nest, do not concat

    return array

def create_menu():

    while True:

        print("")
        print("*****************")
        print(" DATABASE CREATE ")
        print("*****************")
        print("")

        print("OPTIONS: ")
        print("create-stock [VEHICLE TYPE] [NUMBER IN STOCK] [PRICE] [COLOR]")
        print("create-customer [CUSTOMER NAME]")
        print("create-order [CUSTOMER ID] [ORDER LIST]")
        print("back")
        print("")

        user_input = input("What would you like to create today? ")
        user_input = user_input.strip()

        if user_input.startswith("create-order"):
            array = process_list_input(user_input + " ") #trailing space needed for compatability with update-order
        else:
            array = user_input.split(" ")

        try:
            if user_input.startswith("create-customer"):
                name = array[1]

                if len(array) > 2: #additional names
                    for i in range(2, len(array)):
                        name = name + " " + array[i]

                create_customer(name)
                print("Created customer!")
            
            elif user_input.startswith("create-order"):
                customer_id = int(array[1])
                order_list = array.pop()

                customer = get_customer(customer_id)
                for vehicle_id in order_list:
                    adjust_inventory(vehicle_id, -1)

                create_order(customer, order_list, False)
                print("Created order!")
            
            elif user_input.startswith("create-stock"):
                name = array[1]
                in_stock = array[2]
                price = array[3]
                color = array[4]

                create_vehicle(name, in_stock, price, color)
                print("Created new vehicle!")

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
        print("view-order-history [CUSTOMER ID]")
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
            
            elif user_input.startswith("view-order-history"):
                customer_id = array[1]
                customer = get_customer(customer_id)
                orders = CustomerOrder.objects.all()

                for order in orders:
                    if order.customer == customer:
                        print_order(order)
                
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
        print("update-stock [VEHICLE ID] [AMOUNT IN STOCK] [PRICE] [COLOR] [TITLE]")
        print("update-customer [CUSTOMER ID] [NEW NAME]")
        print("update-order [ORDER ID] [ORDER LIST], [BEEN PAID]")
        print("back")
        print("")

        user_input = input("What would you like to update today? ")
        user_input = user_input.strip()

        if not user_input.startswith("update-order"):
            array = user_input.split(" ")
        else: #we have to do something more complicated for an updated order, since that already takes a list as part of its args
            try:
                #command should look something like "update-order 1 [1, 2, 3] no"
                array = process_list_input(user_input)
                array[2] = array[2].upper() #set paid status to upper
            except:
                exception()
                continue #skip the rest of this loop

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

            elif user_input.startswith("update-stock"):
                vehicle_id = int(array[1])
                amount_in_stock = int(array[2])
                price = float(array[3])
                color = array[4]
                vehicle_name = array[5]

                update_vehicle(vehicle_id, amount_in_stock, price, color, vehicle_name)
                print("Updated vehicle!")
            
            elif user_input.startswith("update-customer"):
                customer_id = int(array[1])
                new_name = array[2]

                if len(array) > 3: #additional names
                    for i in range(3, len(array)):
                        new_name = new_name + " " + array[i]

                update_customer(customer_id, new_name)
                print("Updated customer info!")
            
            elif user_input.startswith("update-order"):
                #list should be [command, order id, paid status, [nested order]]
                order_id = array[1]
                paid = False
                order_list = array[3] #nested list

                if array[2] == "YES" or array[2] == "Y" or array[2] == "TRUE":
                    paid = True
                
                update_order(order_id, order_list, paid)
                print("Updated order information!")
            
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
        print("delete-customer [CUSTOMER ID]")
        print("delete-stock [VEHICLE ID]")
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
            
            elif user_input.startswith("delete-customer"):
                customer_id = int(array[1])
                delete_customer(customer_id)
                print("Deleted customer!")

            elif user_input.startswith("delete-stock"):
                vehicle_id = int(array[1])
                delete_vehicle(vehicle_id)
                print("Deleted stock!")

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

            elif user_input == "quit":
                print("Quitting!")
                break

            else:
                exception()
        except:
            exception()

main_menu()