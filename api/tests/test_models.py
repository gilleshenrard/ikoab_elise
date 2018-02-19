from django.test import TestCase
from ..models import Person
from django.contrib.auth.models import User
from ..serializers import PersonSerializer


class PersonTest(TestCase):
    """ Test module for Person model """

    def setUp(self):
        self.john = User.objects.create_user('john', 'test@test.com', 'test', first_name='John', last_name='Doe')
        self.john.person.country='UK'
        self.john.person.phone='+44123456789'
        self.john.person.occupation_field='Diplomacy'
        self.john.person.occupation='Spy'
        self.john.person.birthdate='1963-05-01'
        self.john.person.description='Tall guy'
        self.john.save()
        
        self.jane = User.objects.create_user('jane', 'test2@test.com', 'test', first_name = 'Jane', last_name = 'Dean')
        self.jane.person.country='US'
        self.jane.person.phone='+1123456789'
        self.jane.person.occupation_field='Administration'
        self.jane.person.occupation='Accountance'
        self.jane.person.birthdate='1982-05-01'
        self.jane.person.description='Smart girl'
        self.jane.save()

    def test_valid_person(self):
        user = User.objects.get(first_name='John')
        person_john = Person.objects.get(user=user)
        self.assertEqual(str(person_john), "John")
        
        user = User.objects.get(first_name='Jane')
        person_jane = Person.objects.get(user=user)
        self.assertEqual(str(person_jane), "Jane")
    
    def test_invalid_firstname_person(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(first_name='test')

    def test_valid_serializer_person(self):
        data = {'username' : 'john',
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

        user = User.objects.get(first_name="John")
        data['password'] = user.password
        person = Person.objects.get(user = user)
        serializer = PersonSerializer(person)
        self.assertEqual(data, serializer.data)
        