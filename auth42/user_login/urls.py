from django.urls import path
from . import views

app_name = 'user_login'
urlpatterns = [
	path('dj/login/', views.dj_login, name='dj_login'),
	path('dj/register/', views.dj_register, name='dj_register'),
	path('ft/login/', views.ft_login, name='ft_login'),
	path('ft/login/callback/', views.ft_callback, name='ft_callback'),
]