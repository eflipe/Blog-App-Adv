from django.http import HttpResponse
from django.shortcuts import render
from blog_app.models import Post

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

'''



def post_create(request):
    return HttpResponse("<h1 class="">Create</h1>")


def post_detail(request):
    return HttpResponse("<h1 class="">Detail</h1>")


def post_list(request):
    queryset = Post.objects.all()
    context_data = {
        "obj_list": queryset,
        "title": "List View",
    }
    return render(request, 'index.html', context_data)
    #return HttpResponse("<h1 class="">List</h1>")


def post_update(request):
    return HttpResponse("<h1 class="">Update</h1>")


def post_delete(request):
    return HttpResponse("<h1 class="">Delete</h1>")
