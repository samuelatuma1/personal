from . import views
from django.urls import path

from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index, name='index'),
	path('product/<str:name>/', views.product, name='product'),
	path('item/<str:id>/', views.item, name='item'),
	path('cart/', views.cart, name='cart'),
	path('address/', views.address, name='address' ),
	path('register/', views.register, name='register' ),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 	path('payment/', views.payment, name='payment' ),
  	path('order_placed/', views.order_placed, name='order_placed'),
    path('track_orders/', views.track_orders, name='trackOrders')
]