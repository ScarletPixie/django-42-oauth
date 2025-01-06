from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
	path('dj/login/', views.django_login, name='django_login'),
	path('42/login/', views.login42, name='login'),
	path('42/login/callback/', views.callback42, name='callback'),
]