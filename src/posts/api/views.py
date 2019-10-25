from django.db.models import Q
from rest_framework.filters import(
    SearchFilter,
    OrderingFilter,
)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.generics import( ListAPIView 
,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView)
from posts.models import Post
from.serializers import (PostSerializer,PostDetailSerializer ,PostCreateSerializer)
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(CreateAPIView):
    serializer_class=PostCreateSerializer
    qs=Post.objects.all()
    permission_classes=[IsAuthenticated]
    def perform_create(self,serializer):
        print("................" +str( self.request))
        serializer.save(user=self.request.user)


class PostListAPIView(ListAPIView):
    serializer_class=PostSerializer
    filter_backends=[SearchFilter, OrderingFilter]
    search_fields=['title','content']
    #pagination_class=LimitOffsetPagination
    pagination_class=PostPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        qs_list=Post.objects.all()
       # qs_list=super(PostListAPIView,self).get_queryset(*args,**kwargs)
        query=self.request.GET.get("q")
        if query:
            qs_list=qs_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
            ).distinct()
        return  qs_list

class PostDetailAPIView(RetrieveAPIView):
    serializer_class=PostDetailSerializer
    lookup_field='slug'
    def get_queryset(self):
        qs=Post.objects.all()
        return  qs

class PostUpdateAPIView(UpdateAPIView):
    serializer_class=PostDetailSerializer
    lookup_field='slug'
    permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        qs=Post.objects.all()
        return  qs
   

class PostDeleteAPIView(DestroyAPIView):
    serializer_class=PostDetailSerializer
    lookup_field='slug'
    def get_queryset(self):
        qs=Post.objects.all()
        return  qs

