from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple, CheckboxSelectMultiple
from .models import Post, Category
class PostForm(ModelForm):
    class Meta:
        model = Post

        fields = ['headline', 'text', 'article_default_news',  'categories']
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),

            'article_default_news': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать...'
            }),
            'categories': CheckboxSelectMultiple(attrs={
                'multiple class': 'form-control',
                'class': 'special',
                'size': '100',
            }),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = []