import time
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
from .utils import FtRequest, FtAPIRefreshFail, FtAPINotAvailable, FtAPIForbidden

#	auth_token  {"access_token", "token_type", "expires_in", "refresh_token", "scope", "created_at", "secret_valid_until"}
class RefreshAccessTokenMiddleware:
	EXCLUDED_PATHS = [
		reverse('user_login:ft_login'),
		reverse('user_login:ft_callback'),
	]

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# exclude auth views from token check
		for path in self.EXCLUDED_PATHS:
			if request.path.startswith(path):
				return self.get_response(request)

		# check if token exists and is valid
		token = request.session.get('auth_token')
		if not token or not token.get('access_token') or not token.get('secret_valid_until') or not token.get('refresh_token'):
			return redirect('user_login:ft_login')

		# test token
		response = FtRequest.make_get_request('https://api.intra.42.fr/oauth/token/info', token['access_token'])
		if response.status_code != 200 or int(token.get('secret_valid_until')) < time.time():
			try:
				request.session['auth_token'] = FtRequest.get_refreshed_token(token['refresh_token'])
			# recoverable errors
			except (FtAPIRefreshFail, FtAPIForbidden):
				return redirect('user_login:ft_login')
			# api error (server down, ssl error, timeout etc)
			except (FtAPINotAvailable, Exception) as e:
				return JsonResponse({"error": e}, status=503)
		response = self.get_response(request)
		return response