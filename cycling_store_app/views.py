from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# class InstructorViewSet(viewsets.ModelViewSet):
#     queryset = Instructor.objects.all()
#     serializer_class = InstructorSerializer

#     def create(self, request):
#         mutable_data_copy = request.data.copy()
#         mutable_data_copy['name'] = f'Professor {mutable_data_copy['name']}'
        
#         serializer = InstructorSerializer(data = mutable_data_copy)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)

# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     def retrieve(self, request, pk=None):
#         course = Course.objects.get(pk=pk)
#         course_serializer = CourseSerializer(course)
#         data = course_serializer.data
#         data['instructor_incantation'] = some_function(course)
#         return Response(data)
    
#     def update(self, request, pk=None):
#         course = Course.objects.get(pk=pk)
#         course_serializer = CourseSerializer(data = request.data)
#         course_serializer.is_valid(raise_exception=True)
#         course_serializer.save()
        
#         instructor = Instructor.objects.get(id = course.instructor.id)
#         if (instructor.id == 1):
#             instructor.name = instructor.name + " " + course.name
#             instructor.save()

#         return Response(course_serializer.data)
    
#     def destroy(self, request, pk=None):
#         course = self.get_object()
#         self.perform_destroy(course)
#         return Response()

# def some_function(obj):
#     return "Abracadabra"

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.all()
    serializer_class = OrderSerializer

