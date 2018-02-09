from django.shortcuts import render, get_object_or_404
from web.forms import PersonForm
from api.serializers import PersonSerializer
from django.template.context_processors import request
from django.core.urlresolvers import reverse
from rest_framework.status import HTTP_404_NOT_FOUND
from api.models import Person
import requests

def home(request):
    print("http://localhost:8000" + reverse("get_post_people"))
    r = requests.get("http://localhost:8000" + reverse("get_post_people"))
    return render(request, 'web/home.html', {'people' : r.json()})

def badge(request, FN_search):
    r = requests.get("http://localhost:8000" + reverse("get_post_people"), data={'fstname' : FN_search})
    serializer = PersonSerializer(data=r)
    if serializer.is_valid():
        print(serializer)
        form = PersonForm(request.POST or None, request.FILES, instance=serializer.data)
        print(form)
    
    return HTTP_404_NOT_FOUND

#    person = get_object_or_404(Person, firstname=FN_search)
     
#     form = PersonForm(request.POST or None, request.FILES, instance=r.json())
#     confirm = False
#     if form.is_valid():
#         FN_search=request.POST["firstname"]
#         form.save()
#         confirm = True
#          
#     return render(request, 'web/badge.html', {'form':form, 'FN_search':FN_search, 'confirm':confirm,})