from rest_framework import serializers  
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
User=get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    email2=serializers.EmailField(label='COnfirm Email')
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs={
            "password":{"write_only":True}
        }
    def validate(self,data):
         email= data['email']
         qs=User.objects.filter(email=email)
         if qs.exists():
             raise serializers.ValidationError("user already exists")
         return data 

    def validate_email2(self,value):
         data=self.get_initial()
         email1= data.get('email')
         email2=value
         if email1 != email2:
             raise serializers.ValidationError("email not matches")
         return value

    def create(self,validated_data):
        username=validated_data['username']
        password= validated_data['password']
        email=validated_data['email']
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    token= serializers.CharField(allow_blank=True , read_only=True)
   # email=serializers.EmailField(label='COnfirm Email')
    class Meta:
        model=User
        fields=[
            'username',
            'password',
            'token'
        ]
        extra_kwargs={
            "password":{"write_only":True}
        }

    def validate(self ,data):
        user_obj=None
        username=data.get("username",None)
        password=data['password']
        if not username:
            raise serializers.ValidationError("username not found")

        user=User.objects.filter(username =username).distinct()
        if user.exists( ):
            user = user.first()
        else:
            raise serializers.ValidationError("username is not valid")

        if user_obj:
            if not user_obj .check_password(password):
                raise serializers.ValidationError("incorrect password ")


        data['token']="SOME RANDOM TOKEN"
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
        ]