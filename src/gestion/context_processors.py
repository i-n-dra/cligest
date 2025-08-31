from .views import request_user_role

def user_role_processor(request):
    def get_role():
        return request_user_role(request.user.username)
    return {'request_user_role': get_role}