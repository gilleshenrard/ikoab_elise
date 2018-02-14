from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from rest_framework import status
from api.models import Person
import json

# initialize the APIClient app
client = Client()

class homeTest(TestCase):
    """Test module for values on Home page"""

    def test_get_home(self):
        #get home page with all people
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/home.html')

    def test_get_invalid_home(self):
        #get home page with parameters
        with self.assertRaises(NoReverseMatch):
            client.get(reverse('home', args=['test']))

class badgeTest(TestCase):
    """Test module for values on Badge page"""

    def setUp(self):
        self.john = Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        self.john2 = {
            'firstname' : 'John',
            'lastname' : 'Doe2',
            'country' : 'UK2',
            'email' : 'test2@test.com',
            'phone' : '+441234567892',
            'occupation_field' : 'Diplomacy2',
            'occupation' : 'Spy2',
            'birthdate' : '1963-05-02',
            'description' : 'Tall guy2'}

    def test_valid_get_badge(self):
        response = client.get(reverse('badge', kwargs={'FN_search' : self.john.firstname}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/badge.html')

    def test_invalid_firstname_get_badge(self):
        response = client.get(reverse('badge', kwargs={'FN_search' : 'test'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'web/badge.html')

    def test_valid_post_badge(self):
        response = client.post(reverse('badge', kwargs={'FN_search' : self.john.firstname}), data=json.dumps(self.john2), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/badge.html')
    
    def test_invalid_firstname_post_badge(self):
        response = client.post(reverse('badge', kwargs={'FN_search' : 'test'}), data=json.dumps(self.john2), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTemplateUsed(response, 'web/badge.html')