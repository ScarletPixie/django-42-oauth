import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from urllib.parse import quote
from django.contrib.auth import logout

#	42 AUTH VIEWS
def ft_logout(request):
	logout(request)
	return redirect('user_login:ft_login')

def ft_login(request):
	escaped_url = quote(settings.FT_REDIRECT_URI, safe='')
	formatted_url = f'{settings.FT_LOGIN_URL}?client_id={settings.FT_CLIENT_ID}&redirect_uri={escaped_url}&response_type=code'
	return redirect(formatted_url)

def ft_callback(request):
	authentication_code = request.GET.get('code')

	data = {
		'grant_type': 'authorization_code',
		'client_id': settings.FT_CLIENT_ID,
		'client_secret': settings.FT_CLIENT_SECRET,
		'code': authentication_code,
		'redirect_uri': settings.FT_REDIRECT_URI
	}

	try:
		response = requests.post(settings.FT_TOKEN_URL, data=data)
		if response.status_code == 200:
			token = response.json()
			request.session['auth_token'] = token
			return JsonResponse(token)
		return JsonResponse(response.json())
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)