
from django.conf.urls import url
from django.contrib import admin
from comments.views import (
            comment_thread,
            comment_delete
            
)

urlpatterns = [
     url(r'^detail/(?P<id>\d+)',comment_thread,name= "comment"),
    # url(r'thread/(?P<id>\d+)',comment_thread,name= "comment"),
     url(r'^delete/(?P<id>\d+)', comment_delete,name="delete"),

]
