# from datetime import datetime
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
#
#
# class JWTAuthMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         access_token = request.COOKIES.get('access_token')
#         refresh_token = request.COOKIES.get('refresh_token')
#
#         if access_token:
#             try:
#                 token = AccessToken(access_token)
#                 if datetime.utcfromtimestamp(token['exp']) < datetime.utcnow():
#                     raise TokenError('Token expired')
#
#                 request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
#             except TokenError:
#                 # Попробовать обновить access токен, если refresh токен не истек
#                 new_access_token = self.refresh_access_token(refresh_token)
#
#                 if new_access_token:
#                     request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
#                     request._new_access_token = new_access_token
#                 else:
#                     # Удалить токены из куки, если обновление не удалось
#                     self.clear_cookies(request)
#
#         elif refresh_token:
#             new_access_token = self.refresh_access_token(refresh_token)
#
#             if new_access_token:
#                 request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
#                 request._new_access_token = new_access_token
#             else:
#                 self.clear_cookies(request)
#
#     def refresh_access_token(self, request):
#         try:
#             refresh = RefreshToken(request)
#             new_access_token = str(refresh.access_token)
#             return new_access_token
#         except TokenError:
#             return None
#
#     def process_response(self, request, response):
#         new_access_token = getattr(request, '_new_access_token', None)
#
#         if new_access_token:
#             access_expiry = datetime.utcfromtimestamp(AccessToken(new_access_token)['exp'])
#             response.set_cookie(
#                 key='access_token',
#                 value=new_access_token,
#                 httponly=True,
#                 secure=False,
#                 samesite='Lax',
#                 expires=datetime.utcfromtimestamp(access_expiry),
#             )
#
#         return response
#
#     def clear_cookies(self, request):   # Метод для удаления истекших куки
#         request.COOKIES.pop('access_token', None)
#         request.COOKIES.pop('refresh_token', None)
#         ================================================================

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        if access_token:
            try:
                token = AccessToken(access_token)
                user_id = token.get('user_id')
                if not User.objects.filter(id=user_id).exists():
                    request.bad_token = True
                    return
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                return
            except TokenError:
                pass

        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                user_id = refresh_token.get('user_id')
                if not User.objects.filter(id=user_id).exists():
                    request.bad_token = True
                    return
                new_access_token = refresh_token.access_token
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                request.new_access_token = new_access_token
            except TokenError:
                pass

    def process_response(self, request, response):
        if hasattr(request, 'new_access_token'):
            access_token = request.new_access_token
            access_token_exp = access_token['exp']
            access_token_exp = timezone.datetime.fromtimestamp(
                access_token_exp,
                tz=timezone.get_current_timezone()
            )
            response.set_cookie(
                'access_token', access_token,
                expires=access_token_exp, httponly=True
            )
        if hasattr(request, 'bad_token'):
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
        return response
