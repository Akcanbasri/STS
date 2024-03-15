from django.urls import path
from .views import SignupView, UserDetailView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="sign-up"),
    path("user/", UserDetailView.as_view(), name="user-detail"),
]
