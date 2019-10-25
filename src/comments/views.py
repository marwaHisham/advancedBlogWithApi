from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
# Create your views here.
@login_required#(login_url='/login')
def  comment_delete(request,id):
    obj=get_object_or_404(Comment,id=id)
    try:
        obj=Comment.objects.get(id=id)
    except:
        raise Http404
    if obj.user !=request.user:
        response=HttpResponse("you donot have permission to delete that")
        response.status_code=403
        return response
    if request.method =="POST":
        parent_obj_url=obj.content_object.get_absolute_url()
        obj.delete()
        return HttpResponseRedirect(parent_obj_url)
    context={
        "obj":obj
    }
    return render(request,"confirm_delete.html",context)



def comment_thread(request,id):
    if Comment.objects.filter(id=id).exists()==True:
        obj=get_object_or_404(Comment,id=id)

        if not obj.is_parent:
            obj=obj.parent

        content_object = obj.content_object
        content_id     =  obj.content_object.id

        initial_data={
            "content_type":obj.content_type,
            "object_id":obj.object_id
        }

        form=CommentForm(request.POST or None ,initial= initial_data)
        if form.is_valid() and request.user.is_authenticated():
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
        
        context={
            "obj":obj ,
            "form":form
        }
        return render(request,"comment_thread.html",context)
    else:
        return HttpResponse("no comments")
