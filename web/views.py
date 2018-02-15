from django.shortcuts import render
from web.forms import PersonForm
from django.core.urlresolvers import reverse
from requests import get, put
from rest_framework import status
from django.http.response import HttpResponseNotFound, HttpResponseBadRequest

def home(request):
    r = get("http://localhost:8000" + reverse("get_post_people"))
    if r.status_code == status.HTTP_200_OK:
        return render(request, 'web/home.html', {'people' : r.json()})
    else:
        return HttpResponseNotFound("Badges not found.")

def badge(request, FN_search):
    if request.method == "GET":
        r = get("http://localhost:8000" + reverse("get_delete_update_person", kwargs={'fstname' : FN_search}))
        if r.status_code == status.HTTP_200_OK:
            form = PersonForm(r.json())
            return render(request, 'web/badge.html', {'form':form, 'FN_search':FN_search,})
        else:
            return HttpResponseNotFound("The badge for " + FN_search + " could not be found.")
    
    elif request.method == "POST":
        form = PersonForm(request.POST or None, request.FILES)
        if form.is_valid():
            r = put("http://localhost:8000" + reverse("get_delete_update_person", kwargs={'fstname' : FN_search}), data=request.POST)
            if r.status_code == status.HTTP_404_NOT_FOUND:
                return HttpResponseNotFound("The badge for " + FN_search + " could not be found.")
            elif r.status_code == status.HTTP_400_BAD_REQUEST:
                return HttpResponseBadRequest("Something went wrong")

        return render(request, 'web/badge.html', {'form':form, 'FN_search':FN_search,})