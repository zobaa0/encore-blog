
from django.urls import path
from .import views

app_name = "main"

urlpatterns = [
	path('', views.homepage, name='homepage'),
	path('products', views.products, name='products'),
	path('register', views.register, name='register'),
	path('login', views.login_request, name='login'),
	path('logout', views.logout_request, name='logout'),
	path('blog/<str:tag_page>', views.blog, name='blog'),
	path('user', views.userpage, name='userpage'),
	path('<str:article_page>', views.article, name='article'),
	# path('user', views.userpage, name='userpage'),
]