from django import forms
from .models import Category

class PostSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='All Categories', required=False)