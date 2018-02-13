from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^people/(?P<fstname>[A-z-]{1,32})$',
        views.get_delete_update_person,
        name='get_delete_update_person'),
    url(r'^people/$',
        views.get_post_people,
        name='get_post_people')
]