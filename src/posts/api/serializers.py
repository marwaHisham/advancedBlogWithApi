from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment

class PostSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    comments=serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields=[
            'user',
            'image',
            'title',
            'slug',
            'content',
            'publish',
            'comments'
        ]
    def get_user(self,obj):
        return obj.user.username
    def get_image(self,obj):
        try:
            image= obj.image.path
        except:
            return None
        return image
    def get_comments(self,obj):
        
        c_qs=Comment.objects.filter_by_instace(obj)
        comments=CommentSerializer(c_qs,many=True).data
        return comments


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=[
            'id',
            'user',
            'title',
            'slug',
            'content',
            'publish',
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=[
            'user',
            'title',
            'content',
            'publish',
        ]