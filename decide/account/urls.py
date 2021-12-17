from django.urls import include, path
from account import views

urlpatterns = [
     path('', include('django.contrib.auth.urls')),
     path('singup/', views.signup),
]