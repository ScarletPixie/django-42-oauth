import requests
import secrets
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from urllib.parse import quote
from django.contrib.auth import logout

#	42 AUTH VIEWS
def ft_logout(request):
	url = 'https://api.intra.42.fr/v2/oauth/revoke'
	data = {'token': request.session.get('auth_token').get('access_token'),}
	headers = {'Authorization': f"Bearer {request.session.get('auth_token').get('access_token')}",}
	_ = requests.post(url, data=data, headers=headers)
	logout(request)
	return JsonResponse({'message': 'logout'}, status=200)

def ft_login(request):
	state = secrets.token_urlsafe(128)
	request.session['oauth_state'] = state
	escaped_url = quote(settings.FT_REDIRECT_URI, safe='')
	formatted_url = f'{settings.FT_LOGIN_URL}?client_id={settings.FT_CLIENT_ID}&redirect_uri={escaped_url}&response_type=code&state={state}'
	return redirect(formatted_url)

def ft_callback(request):
	query_state = request.GET.get('state')
	session_state = request.session.get('oauth_state')
	authentication_code = request.GET.get('code')

	if not authentication_code:
		return JsonResponse({'error': 'missing authentication code'}, status=400)
	elif not session_state or query_state != session_state:
		return JsonResponse({'error': 'invalid state'}, status=400)

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