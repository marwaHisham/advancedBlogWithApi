from django.conf.urls import url
from django.contrib import admin
from .views import (
   UserCreateAPIView,UserLoginAPIView
)

urlpatterns = [
     url(r'register',UserCreateAPIView.as_view(),name='register' ),
     url(r'login',UserLoginAPIView.as_view(),name='login' ),

    #  url(r'update/(?P<pk>[-\w\d]+)',CommentUpdateAPIView.as_view(), name="update" ),
    # # url(r'delete/(?P<slug>[-\w\d]+)',CommentDeleteAPIView.as_view(), name="delete" ),
    # url(r'/detail/(?P<pk>\d+)/',CommentDetailAPIView.as_view(), name="comment_detail" ),
    # url(r'/',CommentListAPIView.as_view(), name="commnet_list" ),

]
