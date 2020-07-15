from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):
    # TODO: Define other fields here
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "img",
            "draft",
            "publish"
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        return cleaned_data
