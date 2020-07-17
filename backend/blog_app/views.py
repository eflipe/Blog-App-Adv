from urllib.parse import quote
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from blog_app.models import Post
from comments_app.models import Comment
from comments_app.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm

'''
python manage.py shell

from <app_name> import <model_name>

<model_name>.objects.all()

<model_name>.objects.filter(<field_name>='algo')

<model_name>.objects.filter(<field_name>__icontains='algo')
<model_name>.objects.create(<field_name>="algo algo", <field_name_2>="algo algo 2" )

queryset = <model_name>.objects.all()
for obj in queryset:
    print(obj.<field>)

instance = Post.objects.get(id=1)
'''


def post_create(request):
    form = PostForm(request.POST, request.FILES or None)
    # if not request.user.is_staff or request.user.is_superuser:
    #     raise Http404
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        # print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, 'Cool!')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_create.html", context)


def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    share_string = quote(instance.content)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
            }

    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                                       user=request.user,
                                       content_type=content_type,
                                       object_id=obj_id,
                                       content=content_data,
                                       parent=parent_obj
                                       )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

        if created:
            print("Yeah!")

    comments = Comment.objects.filter_by_instance(instance)

    context = {
        "title": instance.title,
        "obj": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "post_detail.html", context)
    #return HttpResponse("<h1 class="">Detail</h1>")


def post_list(request):
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                        Q(title__icontains=query) |
                        Q(content__icontains=query)

                        )
    paginator = Paginator(queryset_list, 3)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context_data = {
        "obj_list": queryset,
        "title": "List View",
    }
    return render(request, 'post_list.html', context_data)
    #return HttpResponse("<h1 class="">List</h1>")


def post_update(request, id=None):
    # if not request.user.is_staff or request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Kool edit!!!')
        return HttpResponseRedirect(instance.get_absolute_url())

    context_data = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_create.html", context_data)


def post_delete(request, id=None):
    if not request.user.is_staff or request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Delete!!!')
    return redirect('blog_app:index')
