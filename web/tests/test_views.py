from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from rest_framework import status
from api.models import Person
import json
from api.serializers import PersonSerializer
 
# initialize the APIClient app
client = Client()

class getHomeTest(TestCase):
    """Test module for GET requests on Home page"""
  
    def test_get_home(self):
        #get home page with all people
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/home.html')
  
    def test_get_invalid_home(self):
        #get home page with parameters
        with self.assertRaises(NoReverseMatch):
            client.get(reverse('home', args=['test']))

class getBadgeTest(TestCase):
    """Test module for GET requests on Badge page"""
 
    def setUp(self):
        self.john = Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')

    def test_valid_get_badge(self):
        response = client.get(reverse('badge', kwargs={'FN_search' :  'John'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/badge.html')

    def test_invalid_firstname_notexist_get_badge(self):
        response = client.get(reverse('badge', kwargs={'FN_search' : 'test'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTemplateNotUsed("web/badge.html")

class postBadgeTest(TestCase):
    """Test module for POST requests on Badge page"""

    def setUp(self):
        self.john = Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        self.serialiser = PersonSerializer(self.john)
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

    def test_valid_post_badge(self):
        response = client.post(reverse('badge', kwargs={'FN_search' :  self.serialiser.data['firstname']}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/badge.html')
    
    def test_invalid_url_post_badge(self):
        #get badge page with wrong parameters
        with self.assertRaises(NoReverseMatch):
            client.post(reverse('badge', kwargs={'FN_search' : '@@@'}))
     
    def test_invalid_firstname_notexist_post_badge(self):
        response = client.post(reverse('badge', kwargs={'FN_search' : 'test'}), data=self.serialiser.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTemplateNotUsed("web/badge.html")