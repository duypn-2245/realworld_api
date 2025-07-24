from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView
from users import views

urlpatterns = [
    path("api/users/", views.Register.as_view()),
    path("api/users/login/", TokenObtainPairView.as_view()),
    path("api/user/", views.UserInfor.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
