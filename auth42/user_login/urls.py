from django.urls import path
from . import views

app_name = 'user_login'
urlpatterns = [
	#	42 AUTH VIEWS
	path('ft/login/', views.ft_login, name='ft_login'),
	path('ft/login/callback/', views.ft_callback, name='ft_callback'),
	path('ft/profile/', views.ft_profile, name='ft_profile'),
]