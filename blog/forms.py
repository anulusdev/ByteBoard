from django import forms
from .models import Comment, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
    fields = ['name', 'to', "comment"]

class EmailSendForm(forms.Form):
    name = forms.CharField(max_length=50)
    your_email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
    fields = ['name', 'your_email', 'to', "comment"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['body']

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = ['title', 'content', 'status']
        