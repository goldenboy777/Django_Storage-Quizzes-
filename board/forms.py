from django import forms
from django.forms.widgets import CheckboxInput
from .models import Document,Subject


class NewDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document', )



class NewSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name',)

