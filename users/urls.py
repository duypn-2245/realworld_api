from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView
from users import views

urlpatterns = [
    path("api/users/", views.Register.as_view(), name="user-register"),
    path("api/users/login/", TokenObtainPairView.as_view(), name="user-login"),
    path("api/user/", views.UserInfor.as_view(), name="user-infor"),
    path("api/users/<str:username>/", views.Profile.as_view(), name="user-profile"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
