from .models import Task
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
           
    def create(self, validated_data):
        # Automatically assign the user from the context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_active','created_at' ]