from django import forms
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout
)
User=get_user_model()
class UserRegisterForm(forms.ModelForm):
    email=forms.EmailField(label=' Email')
    email2=forms.EmailField(label='confirm Email')
    password=forms.CharField(widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "email2",
            "password"
        
        ]
    def clean_email(self):
        email=self.cleaned_data.get("email")
        email2=self.cleaned_data.get("email2")
        email_qs=User.objects.filter(email=email)
        if email_qs.exists():
             raise forms.ValidationError("email already registered")
 
        return email #super(UserRegisterForm,self).clean(*args,**kwargs)


class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args,**kwargs):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        if username and password:
            if not user:
                raise forms.ValidationError("this user not found")

            if not user.check_password(password):
                raise forms.ValidationError("in correct passowrd")

            if not user.is_active:
                raise forms.ValidationError("this user not active")
            
        return super(UserLoginForm,self).clean(*args,**kwargs)

