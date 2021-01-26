from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Post, User, Category, Comment
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, CategoryForm, AddCommentForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache


class AddComment(CreateView):
    template_name = 'add_comment.html'
    form_class = AddCommentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        id = self.kwargs.get('pk')
        user = self.request.user
        self.object.comment_user = user
        self.object.comment_post_id = id
        self.object.save()
        return super().form_valid(form)


class LikeComment(CreateView):
    form_class = AddCommentForm
    template_name = 'confirm.html'

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        Comment.objects.get(pk=id).like()
        return redirect(f'/news/{Comment.objects.get(pk = id).comment_post.id}')
class DislikeComment(CreateView):
    form_class = AddCommentForm
    template_name = 'confirm.html'

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        Comment.objects.get(pk=id).dislike()
        return redirect(f'/news/{Comment.objects.get(pk = id).comment_post.id}')
class LikePost(CreateView):
    template_name = 'confirm.html'
    form_class = PostForm
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        Post.objects.get(pk=id).like()
        return redirect(f'/news/{id}')

class DislikePost(CreateView):
    template_name = 'confirm.html'
    form_class = PostForm
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        Post.objects.get(pk=id).dislike()
        return redirect(f'/news/{id}')

class CategoryAdd(CreateView):
    template_name = 'subscribe.html'
    model = Category
    queryset = Post.objects.all()
    form_class = CategoryForm


    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(user)
        return redirect('/')
class CategoryRemove(CreateView):
    template_name = 'unsubscribe.html'
    model = Category
    queryset = Category.objects.all()
    form_class = CategoryForm


    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.remove(user)
        return redirect('/')
class AddProtectedView(PermissionRequiredMixin, CreateView):
    template_name = 'add_article.html'
    form_class = PostForm
    login_url='/accounts/login'
    permission_required = ('news.add_post')
    model = Post
    queryset = Post.objects.all()


    def form_valid(self, form):
        self.object = form.save(commit= False)
        author = self.request.user
        id = Author.objects.get(author= User.objects.get(username = str(author))).id
        self.object.author_id = id
        self.object.save()
        return  super().form_valid(form)



class AuthorsList(View):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'author'

class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = PostForm

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=kwargs['queryset'])
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context


class PostDetail(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        user = self.request.user
        context['post_categories'] = Post.objects.get(pk=id).categories.all()
        context['user_categories'] = Category.objects.filter(subscribers= User.objects.get(username=str(user)))
        context['rating'] = Post.objects.get(pk=id).rating_of_post
        context['comments'] = Comment.objects.filter(comment_post=Post.objects.get(pk=id))
        return context


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'add_article.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post')

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SearchDetail(DetailView):
    model = Post
    template_name = 'search_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()








