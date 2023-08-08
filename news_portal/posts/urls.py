from django.urls import path
from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostsList, PostsDetail, PostsListSearch, PostCreate, PostUpdate, PostDelete, subscriptions

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', cache_page(60*1)(PostsList.as_view()), name='posts_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostsDetail.as_view(), name='post_detail'),
    path('search/', PostsListSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
