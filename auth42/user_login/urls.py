from django.urls import path
from . import views

app_name = 'user_login'
urlpatterns = [
	#	42 AUTH VIEWS
	path('login/', views.ft_login, name='ft_login'),
	path('login/callback/', views.ft_callback, name='ft_callback'),
	path('logout/', views.ft_logout, name='ft_logout'),
]