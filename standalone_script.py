import os
import django
from django.conf import settings
# Use this by running:
# python standalone_script.py
os.environ["DJANGO_SETTINGS_MODULE"] = "cycling_store.settings"
django.setup()

print('SCRIPT START *************************')
# Now you have django, so you can import models and do stuff as normal
### NOTE
# DO NOT CHANGE CODE ABOVE THIS LINE
# WORK BELOW

# ===========================================================================================================

# Must Have (DONE)
# ● Have functions in a script to perform CRUD on all models (DONE)

# Should Have (DONE)
# ● Menu of options: (DONE)
    # ○ Order more Vehicles for the store (increase number_in_stock) (DONE)
    # ○ Create a new customer (DONE)
    # ○ Create a customer order (DONE)
        # ■ Removes item from stock (DONE)
    # ○ Display inventory (DONE)
    # ○ Cancel a customer order (DONE)
        # ■ Returns item to stock (DONE)
    # ○ Mark an order paid (DONE)

# Could Have
# ● Extend models with more functionality (DONE)
    # ○ price, different Vehicle types, color, etc. (DONE)
# ● Extend menu of options to handle full CRUD options for each model
# ● Nest menu options for better user flow (DONE)
# ● Display order history for a customer

# Wish List
# ● Add more models to track and manage vehicle components
    # ○ Example: bicycle takes 2 wheels, 1 seat, and 1 handle, etc.
    # ○ Each component could have a price. The total of all the components could be the price of the vehicle.
# ● Ascii Art

# ===========================================================================================================

import datetime
from cycling_store_app.models import *
from crud import *

# create_vehicle("Unicycle", 5)
# create_vehicle("Bicycle", 30)
# create_vehicle("Tricycle", 10)
#print_db(True, False, False)

#create_customer("Maddie Carlson")
#create_customer("Jared Leto")
#print_db(False, True, False)

#create_order(get_customer(1), [get_vehicle(0, "Unicycle"), get_vehicle(0, "Bicycle"), get_vehicle(0, "Tricycle")], datetime.date.today(), True)
#print_db(False, False, True)

#update_vehicle(3, 5)
#update_customer(2, "The Joker")
#update_order(1, [get_vehicle(1)], False)

#create_vehicle("Car", 1)

# delete_vehicle(4)
# delete_customer(2)
# delete_order(4)

print_all()