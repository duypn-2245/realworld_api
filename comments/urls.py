from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from comments import views

urlpatterns = [
    path('api/articles/<slug:slug>/comments/', views.ListComment.as_view()),
    path('api/articles/<slug:slug>/comments/<int:pk>/', views.UpdateDestroyComment.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
