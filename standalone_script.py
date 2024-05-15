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

# Must Have
# ● Have functions in a script to perform CRUD on all models

# Should Have
# ● Menu of options:
    # ○ Order more Vehicles for the store (increase number_in_stock)
    # ○ Create a new customer
    # ○ Create a customer order
        # ■ Removes item from stock
    # ○ Display inventory
    # ○ Cancel a customer order
        # ■ Returns item to stock
    # ○ Mark an order paid

# Could Have
# ● Extend models with more functionality
    # ○ price, different Vehicle types, color, etc.
# ● Extend menu of options to handle full CRUD options for each model
# ● Nest menu options for better user flow
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

#print(get_vehicle(0, "Unicycle"))

#create_customer("Maddie Carlson")

#print_db(False, True, False)

#create_order(get_customer(1), [get_vehicle(0, "Unicycle")], datetime.date.today(), True)

print_db(False, False, True)

#print_all()