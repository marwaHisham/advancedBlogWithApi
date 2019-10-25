
from django.conf.urls import url
from django.contrib import admin
from .views import (
     PostListAPIView  ,
     PostDetailAPIView,
     PostDeleteAPIView,
     PostUpdateAPIView,
     PostCreateAPIView
)

urlpatterns = [
    url(r'/create',PostCreateAPIView.as_view(),name='create' ),
    url(r'/update/(?P<slug>[-\w\d]+)',PostUpdateAPIView.as_view(), name="post_update" ),
    url(r'/delete/(?P<slug>[-\w\d]+)',PostDeleteAPIView.as_view(), name="post_delete" ),
    url(r'/detail/(?P<slug>[-\w\d]+)',PostDetailAPIView.as_view(), name="post_detail" ),
    url(r'/',PostListAPIView.as_view(), name="list" ),

]
