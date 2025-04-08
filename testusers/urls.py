from accounts import views as accounts_custom_views
from django.contrib import admin
from accounts.api import router as accounts_router
from django.urls import path, include
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/accounts/', accounts_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', accounts_custom_views.signup, name="signup_url"),
    # path('accounts/login/', accounts_custom_views.login, name="login_url"),
    path('accounts/', include('allauth.urls'))
    # path('accounts/signup/', signup, name="signup_url"),
]
