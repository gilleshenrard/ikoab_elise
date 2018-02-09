from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_person(request, fstname):
    person = get_object_or_404(Person, firstname=fstname)

    # get details of a single person
    if request.method == 'GET':
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    # delete a single person
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single person
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_people(request):
    # get all people
    if request.method == 'GET':
        people = Person.objects.all()
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data)
    # insert a new record for a person
    elif request.method == 'POST':
        data = {
            'firstname': request.data.get('firstname'),
            'lastname': request.data.get('lastname'),
            'country': request.data.get('country'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'occupation_field': request.data.get('occupation_field'),
            'occupation': request.data.get('occupation'),
            'birthdate': request.data.get('birthdate'),
            'description': request.data.get('description')
        }
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)