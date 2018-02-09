from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
#    url(r'badge/(?P<FN_search>[A-z -]*)$', views.badge, name="badge"),
]