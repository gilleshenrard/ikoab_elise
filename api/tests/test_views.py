import json
from rest_framework import status
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from ..models import Person
from ..serializers import PersonSerializer


# initialize the APIClient app
client = Client()