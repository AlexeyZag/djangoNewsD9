from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
from django.forms import Select, DateTimeInput


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'headline': ['icontains'],
                  'create_time': ['range'],
                  'author': ['exact'],
                  'categories': ['exact'],
                  }
