from django.urls import path

from .views import *

urlpatterns = [
    path("", TodoApiView.as_view()),
    path("work/<int:pk>/", SingleTodoApiView.as_view()),
    path("login/", UserApiView.as_view()),
]