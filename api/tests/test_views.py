import json
from rest_framework import status
from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from ..models import Person
from django.contrib.auth.models import User
from ..serializers import PersonSerializer

# initialize the APIClient app
client = Client()

class MethodsTest(TestCase):
    """Test module for request methods on API"""

    def setUp(self):
        self.john = User.objects.create_user('john', 'test@test.com', 'test', first_name='John', last_name='Doe')
        
    def test_invalid_methods(self):
        #send delete on get_post_people
        response = client.delete(reverse('get_post_people'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        #send put on get_post_people
        response = client.put(reverse('get_post_people'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        #send post on get_delete_update_person
        response = client.post(reverse('get_delete_update_person', kwargs={'fstname': self.john.first_name}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        

class GetAllPeopleTest(TestCase):
    """ Test module for GET all people API """

    def setUp(self):
        self.john = User.objects.create_user('john', 'john@test.com', 'test', first_name='John', last_name='Doe')
        self.john.person.country='UK'
        self.john.person.phone='+44123456789'
        self.john.person.occupation_field='Diplomacy'
        self.john.person.occupation='Spy'
        self.john.person.birthdate='1963-05-01'
        self.john.person.description='Tall guy'
        self.john.save()
        
        self.jane = User.objects.create_user('jane', 'jane@test.com', 'test', first_name = 'Jane', last_name = 'Dean')
        self.jane.person.country='US'
        self.jane.person.phone='+1123456789'
        self.jane.person.occupation_field='Administration'
        self.jane.person.occupation='Accountance'
        self.jane.person.birthdate='1982-05-01'
        self.jane.person.description='Smart girl'
        self.jane.save()

        self.jack = User.objects.create_user('jack', 'jack@test.com', 'test', first_name='Jack', last_name='Damn')
        self.jack.person.country='ES'
        self.jack.person.phone='+34123456789'
        self.jack.person.occupation_field='IT'
        self.jack.person.occupation='Developer'
        self.jack.person.birthdate='1963-05-03'
        self.jack.person.description='Funny guy'
        self.jack.save()
        
        self.jim = User.objects.create_user('jim', 'jim@test.com', 'test', first_name = 'Jim', last_name = 'Done')
        self.jim.person.country='FR'
        self.jim.person.phone='+3323456789'
        self.jim.person.occupation_field='Maintenance'
        self.jim.person.occupation='Janitor'
        self.jim.person.birthdate='1982-05-04'
        self.jim.person.description='Sweet guy'
        self.jim.save()

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
        self.john = User.objects.create_user('john', 'john@test.com', 'test', first_name='John', last_name='Doe')
        self.john.person.country='UK'
        self.john.person.phone='+44123456789'
        self.john.person.occupation_field='Diplomacy'
        self.john.person.occupation='Spy'
        self.john.person.birthdate='1963-05-01'
        self.john.person.description='Tall guy'
        self.john.save()
        
        self.jane = User.objects.create_user('jane', 'jane@test.com', 'test', first_name = 'Jane', last_name = 'Dean')
        self.jane.person.country='US'
        self.jane.person.phone='+1123456789'
        self.jane.person.occupation_field='Administration'
        self.jane.person.occupation='Accountance'
        self.jane.person.birthdate='1982-05-01'
        self.jane.person.description='Smart girl'
        self.jane.save()

        self.jack = User.objects.create_user('jack', 'jack@test.com', 'test', first_name='Jack', last_name='Damn')
        self.jack.person.country='ES'
        self.jack.person.phone='+34123456789'
        self.jack.person.occupation_field='IT'
        self.jack.person.occupation='Developer'
        self.jack.person.birthdate='1963-05-03'
        self.jack.person.description='Funny guy'
        self.jack.save()
        
        self.jim = User.objects.create_user('jim', 'jim@test.com', 'test', first_name = 'Jim', last_name = 'Done')
        self.jim.person.country='FR'
        self.jim.person.phone='+3323456789'
        self.jim.person.occupation_field='Maintenance'
        self.jim.person.occupation='Janitor'
        self.jim.person.birthdate='1982-05-04'
        self.jim.person.description='Sweet guy'
        self.jim.save()

    def test_get_valid_single_person(self):
        response = client.get(
            reverse('get_delete_update_person', kwargs={'fstname': self.john.first_name}))
        user = User.objects.get(first_name = self.john.first_name)
        person = Person.objects.get(user=user)
        serializer = PersonSerializer(person)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_person(self):
        response = client.get(
            reverse('get_delete_update_person', kwargs={'fstname': 'test'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_invalid_single_person_url_type(self):
        with self.assertRaises(NoReverseMatch):
            client.get(reverse('get_delete_update_person', kwargs={'fstname': 30}))
    
    def test_get_invalid_single_person_url_length(self):
        with self.assertRaises(NoReverseMatch):
            client.get(reverse('get_delete_update_person', kwargs={'fstname': "abcdefghijklmnopqrstuvwxyzabcdefg"}))

class CreateNewPersonTest(TestCase):
    """ Test module for inserting a new person """

    def setUp(self):
        self.valid_payload = {'username' : 'john',
                'password' : 'test',
                'firstname' : 'John',
                'lastname' : 'Doe',
                'email' : 'test@test.com',
                'country' : 'UK',
                'phone' : '+44123456789',
                'occupation_field' : 'Diplomacy',
                'occupation' : 'Spy',
                'birthdate' : '1963-05-01',
                'description' : 'Tall guy'
            }
        self.invalid_firstname_payload = {'username' : '@@@@',
                'password' : 'test',
                'firstname' : 'John',
                'lastname' : 'Doe',
                'email' : 'test@test.com',
                'country' : 'UK',
                'phone' : '+44123456789',
                'occupation_field' : 'Diplomacy',
                'occupation' : 'Spy',
                'birthdate' : '1963-05-01',
                'description' : 'Tall guy'
            }
        self.invalid_email_payload = {'username' : 'john',
                'password' : 'test',
                'firstname' : 'John',
                'lastname' : 'Doe',
                'email' : 'test@test.com',
                'country' : 'UK',
                'phone' : '+44123456789',
                'occupation_field' : 'Diplomacy',
                'occupation' : 'Spy',
                'birthdate' : '1963-05-01',
                'description' : 'Tall guy'
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

# class UpdateSinglePersonTest(TestCase):
#     """ Test module for updating an existing person record """
# 
#     def setUp(self):
#         self.john = Person.objects.create(
#             firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
#         self.valid_payload = {
#             'firstname':'John-John',
#             'lastname':'Doe2',
#             'country':'UK2',
#             'email':'test2@test.com',
#             'phone':'+441234567892',
#             'occupation_field':'Diplomacy2',
#             'occupation':'Spy2',
#             'birthdate':'1963-05-02',
#             'description':'Tall guy2'
#         }
#         self.invalid_firstname_payload = {
#             'firstname':'@@@',
#             'lastname':'Doe',
#             'country':'UK',
#             'email':'test@test.com',
#             'phone':'+44123456789',
#             'occupation_field':'Diplomacy',
#             'occupation':'Spy',
#             'birthdate':'1963-05-01',
#             'description':'Tall guy'
#         }
# 
#     def test_valid_update_person(self):
#         response = client.put(
#             reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# 
#     def test_invalid_update_person(self):
#         response = client.put(
#             reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}),
#             data=json.dumps(self.invalid_firstname_payload),
#             content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         
# class DeleteSinglePersonTest(TestCase):
#     """ Test module for deleting an existing person record """
# 
#     def setUp(self):
#         self.john = Person.objects.create(
#             firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
# 
#     def test_valid_delete_person(self):
#         response = client.delete(
#             reverse('get_delete_update_person', kwargs={'fstname': self.john.firstname}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# 
#     def test_invalid_delete_person(self):
#         response = client.delete(
#             reverse('get_delete_update_person', kwargs={'fstname': 'test'}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
# 
#     def test_invalid_delete_person_url(self):
#         with self.assertRaises(NoReverseMatch):
#             client.delete(reverse('get_delete_update_person', kwargs={'fstname': 30}))
#     