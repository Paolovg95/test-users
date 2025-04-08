from ninja import Router
from ninja.security import django_auth

router = Router()
@router.get('/auth', auth=django_auth)
def auth_user(request):
    return f"Authenticated user {request.auth}"
