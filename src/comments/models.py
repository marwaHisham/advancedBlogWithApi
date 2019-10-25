from __future__ import unicode_literals
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models

#from django.core.urlresolvers import reverse

class CommentManager(models.Manager):
    def all(self):
      qs=super(CommentManager,self).filter(parent= None)
      return qs
   
    def create_by_model_type(self,model_type,slug,content,user,parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            some_model = model_qs.first().model_class()
            obj_qs = some_model.objects.filter(slug=slug)

            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

    def filter_by_instace(self,instance):
        content_type=ContentType.objects.get_for_model(instance.__class__)
        obj_id=instance.id
       # Post.objects.get(id=obj.id)
       #super(CommentManager)=Comment.objects
        qs=super(CommentManager,self).filter(content_type=content_type , object_id=obj_id).filter(parent= None)
        #comments= Comment.objects.filter(content_type=content_type , object_id=obj_id)
        return qs



class Comment(models.Model):
     user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,default=1)

     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
     object_id = models.PositiveIntegerField()
     content_object = GenericForeignKey('content_type', 'object_id')
     parent=models.ForeignKey("self",null=True, on_delete=models.CASCADE)
     content= models.TextField()
     timestamp=models.DateTimeField(auto_now=True)

     objects=CommentManager()
     
     class Meta:
       ordering=['timestamp']

     def get_get_absolute_url(self):
         return reverse("comment",kwargs={"id":self.id})


     def __unicode__(self):
        return str(self.user.username)

     def __str__(self):
        return str(self.user.username)

     def children(self):
        return Comment.objects.filter(parent=self)

     @property
     def is_parent(self):
         if self.parent is not None:
            return   False
         return   True