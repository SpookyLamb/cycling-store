from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

import copy

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

