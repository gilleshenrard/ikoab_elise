from django.shortcuts import render
from web.forms import PersonForm
from django.core.urlresolvers import reverse
from requests import get, put
from rest_framework.status import HTTP_400_BAD_REQUEST

def home(request):
    print("http://localhost:8000" + reverse("get_post_people"))
    r = get("http://localhost:8000" + reverse("get_post_people"))
    return render(request, 'web/home.html', {'people' : r.json()})

def badge(request, FN_search):
    if request.method == "GET":
        r = get("http://localhost:8000" + reverse("get_post_people"), data={'fstname' : FN_search})
        form = PersonForm(r.json()[0])
    
    elif request.method == "PUT":
        form = PersonForm(request.POST or None, request.FILES)
        if form.is_valid():
            r = put("http://localhost:8000" + reverse("get_delete_update_person"), args=request.POST, data={'fstname' : FN_search})
            print("BP4")
        else :
            return HTTP_400_BAD_REQUEST
        
    return render(request, 'web/badge.html', {'form':form, 'FN_search':FN_search,})