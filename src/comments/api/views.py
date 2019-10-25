from django.db.models import Q
from rest_framework.filters import(
    SearchFilter,
    OrderingFilter,
)
from rest_framework.mixins import DestroyModelMixin ,UpdateModelMixin
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.generics import( ListAPIView 
,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView)
from comments.models import Comment
from .serializers import (
    CommentSerializer,
    create_comment_serializer,
    CommentChildSerializer,
    CommentDetailSerializer,
    CommentUpdateSerializer
)
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from posts.api.permissions import IsOwnerOrReadOnly
class CommentCreateAPIView(CreateAPIView):
     qs=Comment.objects.all()
     permission_classes=[IsAuthenticated]

     def get_serializer_class(self):
         model_type=self.request.GET.get("type")
         slug=self.request.GET.get("slug")
         parent_id=self.request.GET.get("parent_id")
         print("--"+str(parent_id))

         return create_comment_serializer(
                    model_type='post',
                    slug=slug,
                    parent_id=parent_id,
                    user=self.request.user,

                    )
     

class CommentListAPIView(ListAPIView):
    serializer_class=CommentSerializer
    filter_backends=[SearchFilter, OrderingFilter]
    search_fields=['parent','content']
    #pagination_class=LimitOffsetPagination
    pagination_class=PostPageNumberPagination

    def get_queryset(self,*args,**kwargs):
        qs_list=Comment.objects.all()
       # qs_list=super(CommentListAPIView,self).get_queryset(*args,**kwargs)
        query=self.request.GET.get("q")
        if query:
            qs_list=qs_list.filter(
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
            ).distinct()
        return  qs_list

class CommentDetailAPIView(RetrieveAPIView,DestroyModelMixin,UpdateModelMixin):
    serializer_class=CommentDetailSerializer
    lookup_field='pk'
    def put(self ,request,*args,**kwargs):
         return self.update(request,*args,**kwargs)
    def delete(self ,request,*args,**kwargs):
         return self.destroy(request,*args,**kwargs)
    def get_queryset(self):
        qs=Comment.objects.all()
        return  qs

class CommentUpdateAPIView(RetrieveAPIView,DestroyModelMixin,UpdateModelMixin):
     serializer_class=CommentUpdateSerializer
     lookup_field='pk'
     def put(self ,request,*args,**kwargs):
         return self.update(request,*args,**kwargs)
     def delete(self ,request,*args,**kwargs):
         return self.destroy(request,*args,**kwargs)
     def get_queryset(self):
        qs=Comment.objects.filter(id__gte=0)
        return  qs
   

# class CommentDeleteAPIView(DestroyAPIView):
#     serializer_class=CommentDetailSerializer
#     lookup_field='slug'
#     def get_queryset(self):
#         qs=Comment.objects.all()
#         return  qs

