from django.conf.urls import url
from . import views
from django.views.generic.list import ListView
from api.models import Person

urlpatterns = [
#    url(r'^$', ListView.as_view(model=Person, context_object_name="people", template_name="web/home.html"), name="home"),
#    url(r'badge/(?P<FN_search>[A-z -]*)$', views.badge, name="badge"),
]