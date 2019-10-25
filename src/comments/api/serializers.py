from rest_framework import (
            serializers
            
)
from accounts.api.serializers import UserDetailSerializer
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User=get_user_model()

def create_comment_serializer(model_type=None, slug='None', parent_id=None, user=None):
   
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
               
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            self.user = user
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)
        
        def validate(self,data):
            model_type=self.model_type
            model_qs=ContentType.objects.filter(model=model_type)
            
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("This is not valid content_typt")
            Somemodel=model_qs.first().model_class()
            obj_qs=Somemodel.objects.filter(slug=self.slug)

           # obj_qs=Post.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count()!=1:
                raise serializers.ValidationError("This is not valid slug")
            return data

        def create(self,validated_data):
            content=validated_data.get("content")
            if user:
                main_user=user
            else:
                main_user=User.objects.all().first()
            model_type=self.model_type
            slug=self.slug
            parent_obj=self.parent_obj
            comment=Comment.objects.create_by_model_type(
                model_type=model_type,
                slug=slug,
                user=main_user,
                content=content,
                parent_obj=parent_obj
            )
            return comment

            

    return  CommentCreateSerializer
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Comment
        fields=[
            'id',
            'object_id',
            'content_type',
            'parent',
            'content',
            
        ]
  

class CommentChildSerializer(serializers.ModelSerializer):
    user=UserDetailSerializer()
    class Meta:
        model=Comment
        fields=[
              'id',
              'user',
            'content',
            'timestamp'
            
        ]
class CommentDetailSerializer(serializers.ModelSerializer):
   replies=serializers.SerializerMethodField()
   user=UserDetailSerializer()

   class Meta:
        model=Comment
        fields=[
            'id',
            'object_id',
            'content_type',
            'user',
            'content',
            'replies'
                   
        ]
        read_only_fields=[
            'content_type',
            'object_id',
        ]
   def get_replies(self,obj):
       if obj.is_parent:
           return CommentChildSerializer(obj.children(),many=True).data
       return   None
        




class CommentUpdateSerializer(serializers.ModelSerializer):

   class Meta:
        model=Comment
        fields=[
            'id',
            'content',
            'timestamp'
                   
        ]
  
  
# class CommentCreateSerializer(serializers.ModelSerializer):
#      class Meta:
#          model=Comment
#          fields=[
#              'user',
#              'title',
#              'content',
#              'publish',
#          ]