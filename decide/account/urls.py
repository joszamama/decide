from django.urls import include, path
from account import views

urlpatterns = [
     path('', include('django.contrib.auth.urls')),
     path('signup/', views.signup),
     path('profile/',views.profile)
]