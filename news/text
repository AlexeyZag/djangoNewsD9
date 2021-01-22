python manage.py shell
from news.models import *

1-2) Создаем юзеров и привязываем к ним авторов:

user1 = User.objects.create(username = 'Ivan', first_name = 'Иван')
user2 = User.objects.create(username = 'Alex', first_name = 'Алексей')
Author.objects.create(author = User.objects.get(username = 'Alex'))
Author.objects.create(author = User.objects.get(username = 'Ivan'))

3) Создаем категории:
Category.objects.create(tag = 'Политика')
Category.objects.create(tag = 'Экономика')
Category.objects.create(tag = 'Погода')
Category.objects.create(tag = 'Спорт')

4) Добавляем две статьи и одну новость:
Post.objects.create(author = Author.objects.get(author = User.objects.get(username = 'Ivan')), article_default_news = Post.article, headline = 'выборы президента', text = 'абвгд')
Post.objects.create(author = Author.objects.get(author = User.objects.get(username ='Alex')), article_default_news = Post.news, headline = 'погода сегодня', text = 'Погода сегодня хорошая')
Post.objects.create(author = Author.objects.get(author = User.objects.get(username ='Alex')), article_default_news = Post.article, headline = 'Президент сломал ногу', text = 'Вот это поворот')

5) Присваеваем категории к работам:
p1 = Post.objects.get(headline = "выборы президента")
p2 = Post.objects.get(headline = "погода сегодня")
p3 = Post.objects.get(headline = "Президент сломал ногу")
c1 = Category.objects.get(tag = 'Политика')
c2 = Category.objects.get(tag = 'Экономика')
c3 = Category.objects.get(tag = 'Погода')
c4 = Category.objects.get(tag = 'Спорт')
p1.categories.add(c1, c2)
p2.categories.add(c3)
p3.categories.add(c4)


6) Создаем 4 комментрия:
Comment.objects.create(comment_user = User.objects.get(username= 'Alex'), comment_post = Post.objects.get(headline = 'погода сегодня'), com_text = 'ну ок')
Comment.objects.create(comment_user = User.objects.get(username= 'Ivan'), comment_post = Post.objects.get(headline = 'погода сегодня'), com_text = 'отлично')
Comment.objects.create(comment_user = User.objects.get(username= 'Ivan'), comment_post = Post.objects.get(headline = 'Президент сломал ногу'), com_text = 'старикан')
Comment.objects.create(comment_user = User.objects.get(username= 'Alex'), comment_post = Post.objects.get(headline = 'выборы президента'), com_text = 'ура!')

7) Лайкаем и дислайкаем все новости и комментарии:
Post.objects.get(headline='погода сегодня').like()
Post.objects.get(headline='погода сегодня').like()
Post.objects.get(headline='погода сегодня').like()
Post.objects.get(headline='погода сегодня').like()
Post.objects.get(headline='погода сегодня').like()
Post.objects.get(headline='погода сегодня').dislike()
итого 4 лайка
Post.objects.get(headline='Президент сломал ногу').like()
Post.objects.get(headline='Президент сломал ногу').like()
Post.objects.get(headline='Президент сломал ногу').like()
Post.objects.get(headline='Президент сломал ногу').like()
Post.objects.get(headline='Президент сломал ногу').like()
Post.objects.get(headline='Президент сломал ногу').like()
Post.objects.get(headline='Президент сломал ногу').dislike()
итого 5 лайка
Post.objects.get(headline='выборы президента').like()
Post.objects.get(headline='выборы президента').like()
Post.objects.get(headline='выборы президента').like()
итого 3 лайка

теперь комментарии:
Comment.objects.get(com_text = 'ну ок').like()
Comment.objects.get(com_text = 'ну ок').like()
Comment.objects.get(com_text = 'ну ок').like()
Comment.objects.get(com_text = 'ну ок').like()
Comment.objects.get(com_text = 'отлично').like()
Comment.objects.get(com_text = 'отлично').like()
Comment.objects.get(com_text = 'отлично').like()
Comment.objects.get(com_text = 'старикан').like()
Comment.objects.get(com_text = 'старикан').like()
Comment.objects.get(com_text = 'ура!').like()

8) Обновляем рейтинги пользователей и постов:
Author.objects.get(author= User.objects.get(username ='Alex')).update_rating()
Author.objects.get(author= User.objects.get(username ='Ivan')).update_rating()
проверяем рейтинги
Author.objects.get(author= User.objects.get(username ='Alex')).rating
Author.objects.get(author= User.objects.get(username ='Ivan')).rating

9) Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
top = Author.objects.all().order_by('-rating').values('author', 'rating')[0]
top['author'] = Author.objects.all().order_by('-rating')[0].author.username
print(top)

10) Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
top_post = Post.objects.all().order_by('-rating_of_post').values("create_time", 'author', 'rating_of_post', 'headline')[0]
top_post["create_time"] = top_post["create_time"].strftime("%A, %d. %B %Y %I:%M%p")
top_post['author'] = Post.objects.all().order_by('-rating_of_post')[0].author.author.username
top_post['превью'] = Post.objects.all().order_by('-rating_of_post')[0].preview()
print(top_post)

11) Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье. Выберем статью с двумя комментариями
all_comms = Comment.objects.filter(comment_post =Post.objects.get(headline='погода сегодня')).values('com_time', 'comment_user', 'com_rating', 'com_text')
for com in all_comms:
    com['com_time'] = com['com_time'].strftime("%A, %d. %B %Y %I:%M%p")
    com['comment_user'] = Author.objects.get(author = com['comment_user']).author.username
print(all_comms)
