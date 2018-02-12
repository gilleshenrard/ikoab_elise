import json
from rest_framework import status
from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from ..models import Person
from ..serializers import PersonSerializer

# initialize the APIClient app
client = Client()

class MethodsTest(TestCase):
    """Test module for request methods on API"""

    def setUp(self):
        self.jane = Person.objects.create(
            firstname='Jane', lastname='Dean', country='US', email='test2@test.com', phone='+1123456789', occupation_field='Administration', occupation='Accountance', birthdate='1982-05-01', description='Smart girl')
        Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        
    def test_invalid_methods(self):
        #send delete on get_post_people
        response = client.delete(reverse('get_post_people'))
        self.assertEqual(response, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        #send put on get_post_people
        response = client.put(reverse('get_post_people'))
        self.assertEqual(response, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        #send post on get_delete_update_person
        response = client.post(reverse('get_delete_update_person', kwargs={'fstname': self.jane.firstname}))
        self.assertEqual(response, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        

class GetAllPeopleTest(TestCase):
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

class UpdateSinglePersonTest(TestCase):
    """ Test module for updating an existing person record """

    def setUp(self):
        self.john = Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        self.valid_payload = {
            'firstname':'John-John',
            'lastname':'Doe2',
            'country':'UK2',
            'email':'test2@test.com',
            'phone':'+441234567892',
            'occupation_field':'Diplomacy2',
            'occupation':'Spy2',
            'birthdate':'1963-05-02',
            'description':'Tall guy2'
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

    def test_valid_update_person(self):
        response = client.put(
            reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_person(self):
        response = client.put(
            reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}),
            data=json.dumps(self.invalid_firstname_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class DeleteSinglePersonTest(TestCase):
    """ Test module for deleting an existing person record """

    def setUp(self):
        self.john = Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')

    def test_valid_delete_person(self):
        response = client.delete(
            reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_person(self):
        response = client.delete(
            reverse('get_delete_update_person', kwargs={'fstname': 'test'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_person_url(self):
        with self.assertRaises(NoReverseMatch):
            client.delete(reverse('get_delete_update_person', kwargs={'fstname': 30}))
    