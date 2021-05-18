from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/',views.search, name='search'),
    path('details/<id>', views.details, name='details'),
    path('logout/', views.logout_view, name='logout'),
    path('sign-up/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]
