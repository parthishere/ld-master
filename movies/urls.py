from django.urls import path
from django.conf.urls import url
from . import views

app_name= 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/',views.movie,name='movie'),
    path('series/',views.series,name='series'),
    path('search/',views.search, name='search'),
    path('details/<id>/<g>', views.details, name='details'),
    path('logout/', views.logout_view, name='logout'),
    path('sign-up/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]
