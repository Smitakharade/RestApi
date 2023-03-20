from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from rest_framework import serializers, status
import json

# Create your views here.
@api_view(["GET"])
def get_emp(request, pk=None):        # to get single or all emp
    bytes_data = request.body           # here in this we get data in bytes format
    my_json = bytes_data.decode('utf8').replace("'", '"')   # bytes form data we cant convert to pydict directly so we convert to json first using decode
    py_dict = json.loads(my_json)       # json data is converted into python dictionary
    sid = py_dict.get("id")             # once we get py dict we can access id from it as it is a dict we can use get to fetch an item form a dict
    if sid:                             # this will returns single emp record
        try:    
            emp_obj = Employee.objects.get(id=sid)  # here we get complex data in the form of  queryset 
        except Employee.DoesNotExist:
            return JsonResponse({"msg": "Given id is not present"})
        ser = EmployeeSerializer(emp_obj)       # serializer used to convert complex data to python dict which can be again easily rendered to json
        return JsonResponse(ser.data, status=status.HTTP_200_OK)
        
    all_emp = Employee.objects.all()            # this will return all emp records
    ser = EmployeeSerializer(all_emp, many=True)
    return JsonResponse(ser.data, safe=False)




@api_view(["POST"])
def create_emp(request):
    bytes_data = request.body
    my_json = bytes_data.decode('utf-8').replace("'", '"')
    py_dict = json.loads(my_json)
    ser = EmployeeSerializer(data=py_dict)        
    print(ser)                                  
    if ser.is_valid():  
        data = ser.save()
        return JsonResponse({"msg":"data created successfully", "created data": ser.data}, status=status.HTTP_201_CREATED)
    return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["PUT"])
def update_emp(request):
    bytes_data = request.body
    print(bytes_data)
    my_json = bytes_data.decode('utf8').replace("'", '"')
    py_dict = json.loads(my_json)
    sid = py_dict.get("id")
    if sid:
        e1 = Employee.objects.get(id=sid)
        ser = EmployeeSerializer(instance=e1, data=py_dict)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return JsonResponse({"msg":"data updated successfully", "updated data": ser.data}, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"msg": "Id not found"})


@api_view(["PATCH"])
def partialupdate_emp(request):
    bytes_data = request.body
    my_json = bytes_data.decode('utf8').replace("'", '"')
    py_dict = json.loads(my_json)
    sid = py_dict.get("id")
    e1 = Employee.objects.get(id=sid)
    if sid:
        ser = EmployeeSerializer(instance=e1, data=py_dict, partial=True)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return JsonResponse({"msg":"data partially updated successfully", "updated data": ser.data}, status=status.HTTP_200_OK)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"msg": "Id not found"})


@api_view(["DELETE"])
def delete_emp(request):
    bytes_data = request.body
    my_json = bytes_data.decode('utf8').replace("'", '"')
    py_dict = json.loads(my_json)
    sid = py_dict.get("id")    
    if sid:
        emp = Employee.objects.get(id=sid)
        count = emp.delete()
        return JsonResponse({"msg": "{count}number of employee deleted employee"})
    else:
        emp = Employee.objects.all()
        emp.delete()
        return JsonResponse({"msg": "All record delted successfully"})



# ---------------------------------------------------------------------------------------------
# --------------------------------ALL CRUD OPERATIONS IN A SINGLE VIEW-------------------------
# ----------------------------------------------------------------------------------------------


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def all_crud_operations(request, pk=None):
    if request.method == "GET":
        if pk:
            obj = Employee.objects.get(id=pk)
            ser = EmployeeSerializer(obj)               # only  pass obj directly in get dont  usse data = obj
            return JsonResponse(ser.data, status=status.HTTP_200_OK)
        all_emp  = Employee.objects.all()
        ser = EmployeeSerializer(all_emp, many=True)
        return JsonResponse(ser.data, safe=False)

    elif request.method == "POST":
        py_dict = request.data
        ser = EmployeeSerializer(data=py_dict)          
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return JsonResponse(ser.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == "PUT":
        py_dict = request.data
        pk = py_dict.get("id")
        if pk:
            obj = Employee.objects.get(id=pk)
            ser = EmployeeSerializer(instance=obj, data=py_dict)
            if ser.is_valid():
                data = ser.save()
                data.__dict__.pop("_state")
                return JsonResponse(ser.data, status=status.HTTP_200_OK)
            return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == "PATCH":
        py_dict = request.data
        pk = py_dict.get("id")
        if pk:
            try:
                obj = Employee.objects.get(id=pk)
            except Employee.DoesNotExist:
                return JsonResponse({"msg": "Id not found"})
            ser = EmployeeSerializer(instance=obj, data=py_dict, partial=True)
            if ser.is_valid():
                data = ser.save()
                return JsonResponse(ser.data, status=status.HTTP_200_OK)
            return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)
       

    elif request.method == "DELETE":
        if pk:
            single_emp = Employee.objects.get(id=pk)
            count = single_emp.delete()
            return JsonResponse({"msg": f"{count}number of records deleted successfully"})
        else:
            all_emp = Employee.objects.all().delete()
        return JsonResponse({"msg": "All records are deleted successfully"})


    else:
        return JsonResponse({"msg": "Wrong request"})