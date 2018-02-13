from django.test import TestCase, Client
from django.core.urlresolvers import reverse, NoReverseMatch
from rest_framework import status

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