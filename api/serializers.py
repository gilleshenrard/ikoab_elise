from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    firstname = serializers.CharField(source="user.first_name")
    lastname = serializers.CharField(source="user.last_name")
    password = serializers.CharField(source="user.password")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Person
        fields = ('username', 'password', 'firstname', 'lastname', 'country', 'email', 'phone', 'occupation_field', 'occupation', 'birthdate', 'description')