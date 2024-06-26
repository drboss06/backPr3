from django import forms
from .models import Category
from ckeditor.widgets import CKEditorWidget
from .models import Post

class PostSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='All Categories', required=False)
    
class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['name', 'description', 'featured_image', 'category', 'tags']