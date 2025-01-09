import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings

class FtAPINotAvailable(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)
class FtAPIRefreshFail(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)
class FtAPIForbidden(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


class FtRequest:
	"""
	This is a wrapper class for making requests to the 42 API.

	Dependencies:
		- requests: Must be installed to fetch data from the 42 API.
		- settings.FT_CLIENT_ID: The client id from the 42 app.
		- settings.FT_CLIENT_SECRET: The client secret from the 42 app.
		- settings.FT_REDIRECT_URI: The redirect_uri set in 42 app. Must also be a valid url.
		- settings.FT_TOKEN_URL: The url for fetching an access token.
	"""
	@staticmethod
	def make_get_request(url: str, access_token: str):
		"""
		This method makes a get request to the url provied in the parameter

		Parameters:
			url (str): the url to make the request to.
			access_token (str): a valid access token to be sent in the header.
		Returns:
			A json Response from the 42 API.
		"""
		headers = { 'Authorization': f"Bearer {access_token}" }
		try:
			response = requests.get(url, headers=headers)
			return JsonResponse(response.json(), status=response.status_code)
		except Exception as e:
			return JsonResponse({'error': e})

	@staticmethod
	def get_refreshed_token(auth_token: dict):
		"""
		This method is suppose to receive an existing token taken from the session.

		Parameters:
			auth_token (dict): a valid dict object with these fields {refresh_token}
		Returns:
			dict: a new auth_token  {"access_token", "token_type", "expires_in", "refresh_token", "scope", "created_at", "secret_valid_until"}
		Raises:
			requests.exceptions.RequestException: If the 42 API returns erro,r 500 (internal server error) or 404 (not found)
			requests.exceptions.InvalidHeader: If the request failed with another error (like 401, 403), typically due to missing/invalid header or auth_token parameters.
		"""
		data = {
			'grant_type': 'refresh_token',
			'client_id': settings.FT_CLIENT_ID,
			'client_secret': settings.FT_CLIENT_SECRET,
			'refresh_token': auth_token.get('refresh_token'),
			'redirect_uri': settings.FT_REDIRECT_URI
		}
		try:
			response = requests.post(settings.FT_TOKEN_URL, data=data)
			response.raise_for_status()
		except requests.exceptions.HTTPError as e:
			if response.status_code in [500, 404]:
				raise FtAPINotAvailable(f"The 42 API is currently unavailable, try again later. Details {e}")
			elif response.status_code in [400, 401, 422]:
				raise FtAPIRefreshFail(f"Failed to refresh token. Details {e}")
			elif response.status_code == 403:
				raise FtAPIForbidden(f"Failed to refresh token. Details {e}")
		except Exception as e:
			raise FtAPIRefreshFail(f"Failed to refresh token. Details {e}")
		return response