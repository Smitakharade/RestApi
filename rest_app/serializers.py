from .models import Employee
from rest_framework import serializers
class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    salary = serializers.FloatField()
    date_joined = serializers.DateField()
    is_active = serializers.BooleanField(default=True)
    
    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.salary = validated_data.get("salary", instance.salary)
        instance.date_joined = validated_data.get("date_joined", instance.date_joined)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance