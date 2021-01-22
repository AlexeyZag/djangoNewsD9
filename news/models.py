from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import datetime, date


# Create your models here.




class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_post = 0
        sum_com = 0
        sum_post_com = 0
        auth = self.author
        for i in range(len(Post.objects.filter(author = Author.objects.get(author= User.objects.get(username =auth))))):
            sum_post += Post.objects.filter(author = Author.objects.get(author= User.objects.get(username =auth)))[i].rating_of_post


        user = self.author
        for i in range(len(Comment.objects.filter(comment_user= User.objects.get(username =auth)))):
            sum_com += Comment.objects.filter(comment_user= User.objects.get(username =auth))[i].com_rating

        for post in Post.objects.filter(author = Author.objects.get(author= User.objects.get(username =auth))):
            for comment in Comment.objects.filter(comment_post= Post.objects.filter(headline= post.headline)[0]):
                sum_post_com += comment.com_rating
        self.rating = sum_post * 3 + sum_com + sum_post_com
        self.save()

    def __str__(self):
        return f'{self.author.username}'

class Category(models.Model):
    tag = models.CharField(max_length= 100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True,
                                    related_name='subscription',
                                    verbose_name='Подписчики')

    def __str__(self):
        return f'{self.tag}'


class Post(models.Model):
    article = 'Статья'
    news = 'Новость'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name = "Автор")
    article_default_news = models.CharField(max_length = 7, choices = POSITIONS, default = news, verbose_name= 'Новость или статья')
    create_time = models.DateTimeField(auto_now_add = True, verbose_name= 'Дата создания')
    categories = models.ManyToManyField(Category, through= 'PostCategory', verbose_name= 'Тэг', related_name = 'categories')
    headline = models.CharField(max_length = 255, verbose_name= 'Заголовок')
    text = models.TextField()
    rating_of_post = models.IntegerField(default=0)


    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.id}'


    def like(self):
        self.rating_of_post += 1
        self.save()

    def dislike(self):
        self.rating_of_post -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'



    def __str__(self):
        return f"Автор: {self.author.author.username}, вид работы: {self.article_default_news}, Заголовок: {self.headline}, оценка: {self.rating_of_post}, категории: {self.categories.all()}"


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.category}'

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete = models.CASCADE)
    com_text = models.TextField()
    com_time = models.DateTimeField(auto_now_add = True)
    com_rating = models.IntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()
    def dislike(self):
        self.com_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_post}, {self.comment_user}, {self.com_rating}'



#Category.objects.all().values('subscribers')
#Post.objects.get(pk=id).categories.all().values('tag')
#Category.objects.all()[2].subscribers.all().values('username')
#Category.objects.filter(tag='Спорт').values('subscribers__username').values()
#print(user in Category.objects.filter(tag='Спорт').values('subscribers__username')[0].values())
#Category.objects.get(tag= 'Спорт').subscribers.add(User.objects.get(username='author'))
#Category.objects.all()[0].id
#a = Post.objects.get(pk=4).categories.all().values('tag', 'id')
#a[0]['tag']
#Category.objects.filter(subscribers= User.objects.get(username='admin'))
#Category.objects.filter(subscribers= User.objects.get(username='admin')).values_list()
#Category.objects.filter(subscribers= User.objects.get(username=str(user))).filter(tag = 'Спорт').id
#Category.objects.all().get(pk=1)
#Category.objects.get(pk=1).subscribers.remove(User.objects.get(username='admin'))
#Author.objects.get(author= User.objects.get(username='admin'))
#Author.objects.all()
#Post.objects.get(pk=4).categories.all()
#Category.objects.get(tag=tag).subscribers.all()
#PostCategory.objects.all()
#Post.objects.filter(categories__tag= 'Спорт')
#Post.objects.filter(create_time__gt= datetime.fromtimestamp(datetime.timestamp(datetime.now()) - 604800), categories=tag).values('id')
