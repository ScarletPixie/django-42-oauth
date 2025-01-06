import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse

#	42 AUTH VIEWS
def ft_login(request):
	formatted_url = f'{settings.FT_LOGIN_URL}?client_id={settings.FT_CLIENT_ID}&redirect_uri={settings.FT_REDIRECT_URI}&response_type=code'
	return render(request, 'user_login/login.html', {'FT_LOGIN_URL': formatted_url})

def ft_callback(request):
	authentication_code = request.GET.get('code')

	data = {
		'grant_type': 'authorization_code',
		'client_id': settings.FT_CLIENT_ID,
		'client_secret': settings.FT_CLIENT_SECRET,
		'code': authentication_code,
		'redirect_uri': 'http://localhost:8000/auth/ft/login/callback'
	}

	try:
		response = requests.post('https://api.intra.42.fr/oauth/token', data=data)
		if response.status_code == 200:
			json = response.json()
			print(json)
			request.session['access_token'] = json.get('access_token')
			return redirect(reverse('user_login:ft_profile'))
	
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)

def ft_profile(request):
	access_token = request.session.get('access_token')
	if access_token is None:
		redirect(reverse('user_login:ft_login'))
	try:
		headers = {
			"Authorization": f'Bearer {access_token}',
		}
		response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
		if response.status_code == 200:
			json = response.json()
			print(json)
		return JsonResponse(json, status=200)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)
	return render(request, 'user_login/profile.html', {'username'})

#	DJ LOGIN
#def dj_guest_login(request):
#	pass
