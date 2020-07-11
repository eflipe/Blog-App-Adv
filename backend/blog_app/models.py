from django.db import models
from django.urls import reverse


class Post(models.Model):

    title = models.CharField(blank=True, max_length=120)
    content = models.TextField()
    update = models.DateTimeField(auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id': self.id})
        #return f'/posts/{self.id}/'
