from django.urls import path
from . import views

app_name = 'user_profile'
urlpatterns = [
	path('profile/', views.ft_profile, name='ft_profile')
]