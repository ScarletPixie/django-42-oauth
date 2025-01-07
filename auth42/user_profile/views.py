import requests

from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings

from urllib.parse import quote

# Create your views here.
def ft_profile(request):
	if not request.session.get('auth_token'):
		return redirect('user_login:ft_login')
	try:
		headers = {
			'Authorization': f"Bearer {request.session.get('auth_token')['access_token']}"
		}
		response = requests.get(f'{settings.FT_API_BASE_URL}/me', headers=headers)
		if response.status_code == 401 or response.status_code == 403:
			next = quote(reverse('user_profile:ft_profile'), safe='')
			return redirect(f"{reverse('user_login:ft_refresh')}?refresh_token={request.session.get('auth_token')['refresh_token']}&next={next}")
		elif response.status_code == 500 or response.status_code == 404:
			return JsonResponse({'error': f'error {response.status_code}'}, status=500)
		elif response.status_code == 200:
			return JsonResponse(response.json())
		return JsonResponse({'error': f'error {response.status_code}'}, status=500)
	except Exception as e:
		return JsonResponse({'error': e}, status=500)