from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from rest_framework import status
from api.models import Person

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
        self.jane = Person.objects.create(
            firstname='Jane', lastname='Dean', country='US', email='test2@test.com', phone='+1123456789', occupation_field='Administration', occupation='Accountance', birthdate='1982-05-01', description='Smart girl')
        self.jane = Person.objects.create(
            firstname='Jane', lastname='Dean', country='US', email='test2@test.com', phone='+1123456789', occupation_field='Administration', occupation='Accountance', birthdate='1982-05-01', description='Smart girl')

    def test_valid_get_badge(self):
        response = client.get(reverse('badge', kwargs={'FN_search' : self.jane.firstname}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'web/badge.html')
    
    def test_invalid_method_badge(self):
        response = client.put(reverse('badge', kwargs={'FN_search' : self.jane.firstname}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)