from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    # TODO: Define other fields here

    class Meta:
        model = Post
        fields = [
            "title",
            "content"
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        return cleaned_data
