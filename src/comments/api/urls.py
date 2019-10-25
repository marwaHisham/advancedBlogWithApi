from django.conf.urls import url
from django.contrib import admin
from .views import (
     CommentListAPIView  ,
     CommentDetailAPIView,
    #  CommentDeleteAPIView,
      CommentUpdateAPIView,
      CommentCreateAPIView
)

urlpatterns = [
     url(r'create',CommentCreateAPIView.as_view(),name='comment_create' ),
     url(r'update/(?P<pk>[-\w\d]+)',CommentUpdateAPIView.as_view(), name="update" ),
    # url(r'delete/(?P<slug>[-\w\d]+)',CommentDeleteAPIView.as_view(), name="delete" ),
    url(r'/detail/(?P<pk>\d+)/',CommentDetailAPIView.as_view(), name="comment_detail" ),
    url(r'/',CommentListAPIView.as_view(), name="commnet_list" ),

]
