from django import forms
from .models import Task

class TodoForm(forms.Form):
    description = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control m-auto',
        'placeholder': 'Add a new todo...'
    }))

class EditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description']


