from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout
)
from django.http import HttpResponse,HttpResponseRedirect,Http404

from.forms import UserLoginForm,UserRegisterForm

from django.shortcuts import render

# Create your views here.

def login_view(request):
    next=request.GET.get('next')
    title="Login"
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        login(request,user)
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect("/posts/list")

    context={
        "form":form,
        "title":title
    }
    return render(request,"loginform.html",context)

def register_view(request):
    next=request.GET.get('next')
    title="Register"
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user=authenticate(username=user.username,password=password)
        login(request,new_user)
        if next:
            return HttpResponseRedirect(next)

        return HttpResponseRedirect("/posts/list")
    context={
        "form":form,
        "title":title,
    }
    return render(request,"form.html",context)

def logout_view(request):
    logout(request)
    return HttpResponse("<h1>user logout </h1>")
