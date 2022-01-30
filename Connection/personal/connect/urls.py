from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.sign_up, name='sign_up'),
    path("signout/", views.sign_out, name='sign_out'),
    path("signin/", views.sign_in, name='sign_in'),
    path("", views.index, name='index'),
    path("search/", views.search, name='search'),
    path('add/<int:id>/', views.add_friend, name='add_friend'),
    path('find_skill/', views.find_skill, name='find_skill'),
    path('friends/', views.friends, name='friends')
]