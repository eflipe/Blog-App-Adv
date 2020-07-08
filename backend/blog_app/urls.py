from django.urls import path
from blog_app.views import (
    post_create,
    post_list,
    post_delete,
    post_detail,
    post_update,
    )

urlpatterns = [
    path('', post_list),
    path('create/', post_create),
    path('delete/', post_delete),
    path('update/', post_update),
    path('detail/', post_detail),
]
