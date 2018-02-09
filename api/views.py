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
        return Response({})
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
        return Response({})
    # insert a new record for a person
    elif request.method == 'POST':
        return Response({})