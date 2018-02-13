from django.shortcuts import render
from web.forms import PersonForm
from django.core.urlresolvers import reverse
from requests import get, put

def home(request):
    r = get("http://localhost:8000" + reverse("get_post_people"))
    return render(request, 'web/home.html', {'people' : r.json()})

def badge(request, FN_search):
    if request.method == "GET":
        r = get("http://localhost:8000" + reverse("get_delete_update_person", kwargs={'fstname' : FN_search}))
        form = PersonForm(r.json())
        return render(request, 'web/badge.html', {'form':form, 'FN_search':FN_search,})
    
    elif request.method == "POST":
        form = PersonForm(request.POST or None, request.FILES)
        if form.is_valid():
            r = put("http://localhost:8000" + reverse("get_delete_update_person", kwargs={'fstname' : FN_search}), data=request.POST)
        return render(request, 'web/badge.html', {'form':form, 'FN_search':FN_search,})