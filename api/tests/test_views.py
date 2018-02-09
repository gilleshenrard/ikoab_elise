import json
from rest_framework import status
from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from ..models import Person
from ..serializers import PersonSerializer


# initialize the APIClient app
client = Client()

class GetAllPuppiesTest(TestCase):
    """ Test module for GET all people API """

    def setUp(self):
        Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        Person.objects.create(
            firstname='Jane', lastname='Dean', country='US', email='test2@test.com', phone='+1123456789', occupation_field='Administration', occupation='Accountance', birthdate='1982-05-01', description='Smart girl')
        Person.objects.create(
            firstname='Jack', lastname='Dull', country='FR', email='test3@test.com', phone='+33123456789', occupation_field='Maintenance', occupation='Welder', birthdate='1973-05-01', description='Cool guy')
        Person.objects.create(
            firstname='Jim', lastname='Dane', country='ES', email='test4@test.com', phone='+3423456789', occupation_field='IT', occupation='Developer', birthdate='1989-05-01', description='Smart guy')

    def test_get_all_people(self):
        # get API response
        response = client.get(reverse('get_post_people'))
        # get data from db
        people = Person.objects.all()
        serializer = PersonSerializer(people, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class GetSinglepersonTest(TestCase):
    """ Test module for GET single person API """

    def setUp(self):
        self.john = Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        self.jane = Person.objects.create(
            firstname='Jane', lastname='Dean', country='US', email='test2@test.com', phone='+1123456789', occupation_field='Administration', occupation='Accountance', birthdate='1982-05-01', description='Smart girl')
        self.jack = Person.objects.create(
            firstname='Jack', lastname='Dull', country='FR', email='test3@test.com', phone='+33123456789', occupation_field='Maintenance', occupation='Welder', birthdate='1973-05-01', description='Cool guy')
        self.jim = Person.objects.create(
            firstname='Jim', lastname='Dane', country='ES', email='test4@test.com', phone='+3423456789', occupation_field='IT', occupation='Developer', birthdate='1989-05-01', description='Smart guy')

    def test_get_valid_single_person(self):
        response = client.get(
            reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}))
        person = Person.objects.get(firstname = self.john.firstname)
        serializer = PersonSerializer(person)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_person(self):
        response = client.get(
            reverse('get_delete_update_person', kwargs={'fstname': 'test'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_invalid_single_person_url(self):
        with self.assertRaises(NoReverseMatch):
            client.get(reverse('get_delete_update_person', kwargs={'fstname': 30}))

class CreateNewPersonTest(TestCase):
    """ Test module for inserting a new person """

    def setUp(self):
        self.valid_payload = {
            'firstname':'John',
            'lastname':'Doe',
            'country':'UK',
            'email':'test@test.com',
            'phone':'+44123456789',
            'occupation_field':'Diplomacy',
            'occupation':'Spy',
            'birthdate':'1963-05-01',
            'description':'Tall guy'
        }
        self.invalid_firstname_payload = {
            'firstname':'@@@',
            'lastname':'Doe',
            'country':'UK',
            'email':'test@test.com',
            'phone':'+44123456789',
            'occupation_field':'Diplomacy',
            'occupation':'Spy',
            'birthdate':'1963-05-01',
            'description':'Tall guy'
        }
        self.invalid_email_payload = {
            'firstname':'John',
            'lastname':'Doe',
            'country':'UK',
            'email':'test',
            'phone':'+44123456789',
            'occupation_field':'Diplomacy',
            'occupation':'Spy',
            'birthdate':'1963-05-01',
            'description':'Tall guy'
        }

    def test_create_valid_person(self):
        response = client.post(
            reverse('get_post_people'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_person_firstname(self):
        response = client.post(
            reverse('get_post_people'),
            data=json.dumps(self.invalid_firstname_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_person_email(self):
        response = client.post(
            reverse('get_post_people'),
            data=json.dumps(self.invalid_email_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    