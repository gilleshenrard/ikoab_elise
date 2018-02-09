from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<fstname>[A-z -]*)$',
        views.get_delete_update_person,
        name='get_delete_update_person'),
    url(r'^/$',
        views.get_post_people,
        name='get_post_people')
]