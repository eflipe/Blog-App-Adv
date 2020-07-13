from django.urls import path
from blog_app.views import (
    post_create,
    post_list,
    post_delete,
    post_detail,
    post_update,
    )

app_name = 'blog_app'

urlpatterns = [
    path('', post_list, name='index'),
    path('create/', post_create),
    path('<id>/delete/', post_delete, name='delete'),
    path('<id>/edit/', post_update, name='update'),
    path('<id>/', post_detail, name='detail'),
]
