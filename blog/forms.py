from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Your comment', 'rows': 4}))
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'featured_image', 'excerpt', 'content', 'status', 'tags']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 10

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'featured_image', 'excerpt', 'content', 'status', 'tags']

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 10
