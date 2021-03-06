from urllib.parse import quote
from django.shortcuts import( render,get_object_or_404,redirect)
from django.http import( HttpRequest,HttpResponse,HttpResponseRedirect,Http404)
from django.contrib.contenttypes.models import ContentType
from  .models import Post
from comments.models import Comment
from django.utils import timezone

from .forms import PostForm
from comments.forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def post_create(request):

    if not request.user.is_authenticated  :
        print ("not=========")
        HttpResponseRedirect("/login")
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form=PostForm(request.POST or None ,request.FILES or None )
    if form.is_valid():
         instance=form.save(commit=False)
         instance.save()
         messages.success(request,"successfly updated")
         return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"not accepted")
    context={
        "form":form
    }
    return render(request,"posts_create.html",context)
    
    # if request.method=="POST":
    #      title=request.POST.get("title")
    #      content=request.POST.get("content")
    #      Post.objects.Create(title=title,content=content)
    #      Post.save()
    #      print(request.POST)
   

def post_details(request,slug=None):
   # obj=get_object_or_404(Post,id=51)
    if Post.objects.filter(slug=slug).exists()==True:
        obj=get_object_or_404(Post,slug=slug)
        #obj=Post.objects.active(slug=slug)
        share_string=quote(obj.content)

        initial_data={
            "content_type":obj.get_content_type,
            "object_id":obj.id
        }

        form=CommentForm(request.POST or None ,initial= initial_data)
        if form.is_valid():
            c_type=form.cleaned_data.get("content_type")
            content_type=ContentType.objects.get(model=c_type)
            obj_id=form.cleaned_data.get('object_id')
            content_data=form.cleaned_data.get('content')
            parent_obj=None
            try:
               parent_id=int(request.POST.get("parent_id"))
            except:
                parent_id=None

            if parent_id:
                parent_qs=Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj =parent_qs.first()

              
            new_comment,created=Comment.objects.get_or_create(
               user=request.user,
               content_type=content_type,
               object_id=obj_id,
               content=content_data,
               timestamp=timezone.now(),
               parent=parent_obj
            )
           
              
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
            
       
        comments=obj.comments
        usernow=request.user
        context={
            "obj":obj ,
            "share_string":share_string,
            "comments":comments,
            "comment_form":form,
            'usernow':usernow

        }
        return render(request,"posts_detail.html",context)
    else:
         return HttpResponse("no obj")


def post_list(request):
    if not request.user.is_authenticated  :
        print ("not=========")
        return HttpResponseRedirect("/login")
    else:
        #obj=Post.objects.all().order_by("updated")
        obj = Post.objects.active().filter(draft = False)
        query= request.GET.get("q")
        if query:
            obj=obj.filter(Q(title__icontains=query)|
            Q(content__icontains=query)
            ).distinct()

        paginator = Paginator(obj, 3) # Show 25 contacts per page
        #search
    
        page = int(request.GET.get('page', '1'))
        contacts = paginator.page(page)
        if request.user.is_authenticated :
            print(request.user)
            context={"obj":contacts}
        else:
            context={"obj":"un authorized user"}
        return render(request,"posts_list.html",context)

def post_update(request,slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,request.FILES or None , instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request,"successfly updated")
        return redirect('detail',slug)
    
    template_name = 'posts_create.html'
    context = {"title":"{obj.title}", "form": form}
    return render(request, template_name, context)  
    # if Post.objects.filter(id=post_id).exists()==True:
    #     instance=Post.objects.get(id=post_id)
    # form=PostForm(request.POST or None ,instance=instance)
    # if form.is_valid:
    #     instance=form.save(commit= False)
    #     instance.save()
    # return redirect('detail', self.object.pk)
    # context={
    #     "title":instance.title,
    #     "instance":instance,
    #     "form":form
    # }
    # return render(request,"posts_create.html",context)

def post_delete(request,id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    messages.success(request,"successfly deleted")
    return redirect("posts/list")
    