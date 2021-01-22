from django.urls import path
from.views import AuthorsList, AuthorDetail, PostList, PostDetail, SearchList, SearchDetail, PostUpdateView, PostDeleteView, AddProtectedView, CategoryAdd, CategoryRemove
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    path('', PostList.as_view(), name = 'post_list'),
    path('<int:pk>', PostDetail.as_view(), name= 'post_detail'),
    path('authors', AuthorsList.as_view(), name= 'authors'),
    path('authors/<int:pk>/', AuthorDetail.as_view()),
    path('search', SearchList.as_view(), name= 'search'),
    path('search/<int:pk>', SearchDetail.as_view(), name= 'search_detail'),
    path('add/', AddProtectedView.as_view(), name= 'add_post'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name= 'post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name= 'post_delete'),
    path('subscribe/<int:pk>', CategoryAdd.as_view(), name= 'subscribe'),
    path('unsubscribe/<int:pk>', CategoryRemove.as_view(), name= 'unsubscribe'),
    #path('appointment/', AppointmentView.as_view(), name= 'appointments'),

]


