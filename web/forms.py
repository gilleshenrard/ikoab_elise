from django.forms import ModelForm
from api.models import Person
from django.forms.fields import TextInput
from django.forms.widgets import Textarea, EmailInput, DateInput
    
class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('id',)
        widgets = {
            'firstname':TextInput(attrs={'class':'form-control'}),
            'lastname':TextInput(attrs={'class':'form-control'}),
            'country':TextInput(attrs={'class':'form-control'}),
            'email':EmailInput(attrs={'class':'form-control'}),
            'phone':TextInput(attrs={'class':'form-control', 'type':'tel'}),
            'occupation_field':TextInput(attrs={'class':'form-control'}),
            'occupation':TextInput(attrs={'class':'form-control'}),
            'birthdate':DateInput(attrs={'class':'form-control', 'type':'date'}),
            'description':Textarea(attrs={'class':'form-control', 'rows':'5'}),
            }