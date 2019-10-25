
from django.conf.urls import url,include
from django.contrib import admin
from posts.views import (
            post_create,
            post_delete
            ,post_details
            ,post_list
            ,post_update
)

urlpatterns = [
    url(r'list/',post_list, name="list" ),
    url(r'^create/',post_create ),
    url(r'^detail/(?P<slug>[-\w\d]+)',post_details,name= "detail"),
    url(r'^update/(?P<slug>[-\w\d]+)',post_update ,name="update" ),
    url(r'^delete/(?P<id>\d+)',post_delete ,name="delete"),


]
