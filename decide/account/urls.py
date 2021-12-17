from django.urls import include, path
from account import views

urlpatterns = [
     path('login/', views.view_login),
     path('signup/', views.signup),
     path('profile/',views.profile)
]