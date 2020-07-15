from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)


def upload_location(instance, filename):
    return f'{instance.id}/{filename}'


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=120, null=True)
    slug = models.SlugField(unique=True)
    img = models.ImageField(upload_to=upload_location,
                            blank=True,
                            null=True,
                            height_field="height_field",
                            width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(null=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now_add=False)
    update = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ["-id", "-timestamp", "-update"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:detail', kwargs={'id': self.id})
        #return f'/posts/{self.id}/'


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        slug = f'{slug}-{instance.id}'
    instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Post)
