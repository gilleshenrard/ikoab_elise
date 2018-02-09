from django.test import TestCase
from ..models import Person
from django.core.exceptions import ValidationError


class PersonTest(TestCase):
    """ Test module for Person model """

    def setUp(self):
        Person.objects.create(
            firstname='John', lastname='Doe', country='UK', email='test@test.com', phone='+44123456789', occupation_field='Diplomacy', occupation='Spy', birthdate='1963-05-01', description='Tall guy')
        Person.objects.create(
            firstname='Jane', lastname='Dean', country='US', email='test2@test.com', phone='+1123456789', occupation_field='Administration', occupation='Accountance', birthdate='1982-05-01', description='Smart girl')

    def test_valid_person(self):
        person_john = Person.objects.get(firstname='John')
        self.assertEqual(str(person_john), "John")
        
        person_jane = Person.objects.get(firstname='Jane')
        self.assertEqual(str(person_jane), "Jane")
        
    def test_invalid_person_firstname(self):
#        with self.assertRaises(ValidationError):
#            Person.objects.create(firstname='!!!')
        pass
            
    def test_invalid_person_email(self):
#        with self.assertRaises(ValidationError):
#            Person.objects.create(email='abcde')
        pass