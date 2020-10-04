from django.urls import path

from . import views

urlpatterns = [
    path('callback/<slug:appid>/', views.CallbackView.as_view()),
]
