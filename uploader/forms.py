from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["file", "text"]  # adjust if you have title/other fields

class QueryForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea, max_length=2000)
