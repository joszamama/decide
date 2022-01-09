from django.urls import include, path
from django.contrib.auth.views import logout
from account import views
from authentication.views import LogoutView

urlpatterns = [
     path('login/', views.view_login),
     path('signup/', views.signup),
     path('profile/',views.profile),
     path('mivotacion/',views.misvotaciones),
     path('update/',views.updateUser),
     path('', include('social_django.urls', namespace='social')),
     path('logout/', logout, name='logout'),
]