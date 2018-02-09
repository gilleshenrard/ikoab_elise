from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('firstname', 'lastname', 'country', 'email', 'phone', 'occupation_field', 'occupation', 'birthdate', 'description')