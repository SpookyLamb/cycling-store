from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# import copy
# import json

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        #remove vehicles from inventory

        order_list = request.data.getlist('order')

        for vehicle_id in order_list:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.number_in_stock -= 1
            vehicle.save()
        
        serializer = OrderSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        #add/remove vehicles to/from inventory
        #combination of what is done for destroy and create

        #grab the original order list
        order = self.get_object()
        og_order_list = order.order.values_list('pk', flat=True) #grabs a queryset with vehicle ids
        og_order_list = list(og_order_list) #turn it into a list

        for vehicle_id in og_order_list: #add all of those vehicles back to inventory
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.number_in_stock += 1
            vehicle.save()

        #grab the new order list, remove the vehicles in it
        order_list = request.data.getlist('order')

        for vehicle_id in order_list:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.number_in_stock -= 1
            vehicle.save()
        
        serializer = OrderSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        #add vehicles back to inventory

        order = self.get_object()
        order_list = order.order.values_list('pk', flat=True) #grabs a queryset with vehicle ids
        order_list = list(order_list) #turn it into a list

        for vehicle_id in order_list:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.number_in_stock += 1
            vehicle.save()
        
        self.perform_destroy(order)
        return Response()

class SalesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    #displays the following information:
        # Total number of vehicles (DONE)
        # Number of vehicles by type (DONE)
        # Total number of customers (DONE)
        # Number of customers who have purchased a vehicle (DONE)
        # Average vehicles per customer (DONE)

    queryset = Vehicle.objects.all()

    def list(self, request):
        #needs to return JSON data via a Response() class
        #this data can be manipulated to do what we want

        queryset = Vehicle.objects.all() 
        vehicle_list = list(queryset)
        
        vehicle_count = 0 #total vehicles
        vehicles_by_type = {} #total vehicles by TYPE

        for vehicle in vehicle_list:
            vehicle_count += vehicle.number_in_stock
            vehicles_by_type[vehicle.type] = vehicle.number_in_stock
        
        queryset = Customer.objects.all()
        customer_list = list(queryset)
        customer_count = len(customer_list) #grab customer count

        #sum customers who have purchased at least one vehicle
        #can be done by matching them to orders
        queryset = CustomerOrder.objects.all()
        order_list = list(queryset)
        customers_with_orders = []
        vehicles_sold = 0 #a secret tool that will help us later

        for order in order_list:
            customer = order.customer
            if not customer in customers_with_orders:
                customers_with_orders.append(customer)
            
            vehicles_ordered = order.order.values_list('pk', flat=True) #grabs a queryset with vehicle ids
            vehicles_ordered = list(vehicles_ordered) #turn it into a list
            vehicles_sold += len(vehicles_ordered) #add length
        
        customer_with_orders_count = len(customers_with_orders)
        
        #average vehicles purchased per customer
        avg_purchases = vehicles_sold / customer_count

        dictionary = {
            "Vehicle Count": vehicle_count,
            "Vehicles By Type": vehicles_by_type,
            "Customer Count": customer_count,
            "Customers With Purchases": customer_with_orders_count,
            "Average Purchases Per Customer": avg_purchases,
        }

        return Response(dictionary)
