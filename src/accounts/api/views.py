from django.db.models import Q
from rest_framework.filters import(
    SearchFilter,
    OrderingFilter,
)
from rest_framework.mixins import DestroyModelMixin ,UpdateModelMixin
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.generics import( 
    ListAPIView 
   ,CreateAPIView,
   RetrieveAPIView,
   UpdateAPIView,
   DestroyAPIView
   )
from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
   
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from posts.api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST

User=get_user_model()
class UserCreateAPIView(CreateAPIView):
    serializer_class=UserCreateSerializer
    qs= User.objects.all()



class UserLoginAPIView(CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=UserLoginSerializer
    def post(self ,request,*args, **kwargs):
        data=request.data
        serializer_class=UserLoginSerializer(data=data)
        if serializer_class.is_valid(raise_exception=True):
            new_data=serializer_class.data
            return Response(new_data ,status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
