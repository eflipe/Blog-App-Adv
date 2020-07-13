from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from blog_app.models import Post
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
    form = PostForm(request.POST)

    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, 'Cool!')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Err!')

    context = {
        "form": form,
    }
    return render(request, "post_create.html", context)


def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "obj": instance,
    }
    return render(request, "post_detail.html", context)
    #return HttpResponse("<h1 class="">Detail</h1>")


def post_list(request):
    queryset = Post.objects.all()
    context_data = {
        "obj_list": queryset,
        "title": "List View",
    }
    return render(request, '_base.html', context_data)
    #return HttpResponse("<h1 class="">List</h1>")


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)

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
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Delete!!!')
    return redirect('blog_app:index')
