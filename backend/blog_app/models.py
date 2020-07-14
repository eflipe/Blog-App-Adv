from django.db import models
from django.urls import reverse


class Post(models.Model):

    title = models.CharField(blank=True, max_length=120, null=True)
    content = models.TextField(null=True)
    update = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ["-id", "-timestamp", "-update"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:detail', kwargs={'id': self.id})
        #return f'/posts/{self.id}/'
