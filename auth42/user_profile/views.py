from django.conf import settings
from ft_utils.utils import FtRequest

# Create your views here.
def ft_profile(request):
	access_token = request.session.get('auth_token').get('access_token')
	response = FtRequest.make_get_request(f'{settings.FT_API_BASE_URL}/me', access_token)
	return response