from django import forms

from pagedown.widgets import PagedownWidget

from .models import Comment

class CommentForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    content=forms.CharField(widget=forms.TextInput)
    class Meta:
        model = Comment
        fields = [
            "content",
        ]