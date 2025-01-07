from django.urls import path
from . import views

app_name = 'user_login'
urlpatterns = [
	#	42 AUTH VIEWS
	path('login/', views.ft_login, name='ft_login'),
	path('login/callback/', views.ft_callback, name='ft_callback'),
	path('login/refresh/', views.ft_refresh, name='ft_refresh')
]