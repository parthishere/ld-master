from configparser import ConfigParser
import tmdbsimple as tmdb
import tmdbv3api as tmdb1
import os




from django.shortcuts import render, Http404, get_object_or_404, get_list_or_404, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile
from . forms import LoginForm


config = ConfigParser()
config.read('movies/config.cfg')
tmdb.API_KEY = config['tmdb']['API_KEY']


def home(request):
    """This is a function-based view to serve
    the movie list for a particular search query,
    using tmdbsimple API calls.

    Params:
        request: request from the front-end API call

    Returns:
        render method at the movie.html endpoint with
        the required search results.
    """
    query = str(request.GET.get('query', ''))
    popular_movie_tmdb = tmdb.Movies('popular')
    popular_movie = popular_movie_tmdb.info()['results'][:5]

    top_rated_tv_tmdb = tmdb.TV('top_rated')
    top_rated_tv = top_rated_tv_tmdb.info()['results'][:5]

    return render(request, "home_page.html", {'popular_movie':popular_movie, 'top_rated_tv':top_rated_tv})

def search(request):
     query = str(request.GET.get('query', ''))
     if query != '':
        search_result = tmdb.Search().multi(query=query)['results']
        frontend = {
            "search_result": sorted(search_result, key=lambda x: x['popularity'], reverse=True),
            "has_result": (search_result != [])
        }
     else:
        frontend = {
            "search_result": [],
            "has_result": False
        }
     return render(request, "movie.html",frontend)
def details(request, id=None, g=None):
    """This is a function-based view to serve 
    the movie details for a particular list click,
    using tmdbsimple API calls.

    Params:
        request: request from the front-end API call
        id (int): id of the movie clicked on

    Returns:
        render method at the details.html endpoint with
        the required movie details.
    """
    if g=='m':
        movie = tmdb.Movies(id)
        trailers = list(filter(lambda v: v['type'] == 'Trailer', movie.videos()['results']))
        teasers = list(filter(lambda v: v['type'] == 'Teaser', movie.videos()['results']))
        keywords = movie.keywords()['keywords']
        from pprint import pprint
        pprint(movie.reviews()['results'])
        frontend = {
            "info": movie.info(),
            "year": movie.info()['release_date'][:4],
            "cast": movie.credits()['cast'][:15],
            "crew": movie.credits()['crew'][:15],
            "trailers": trailers,
            "teasers": teasers,
            "keywords": keywords,
            "reviews": movie.reviews()['results'],
            "alt": movie.alternative_titles()['titles']
        }
    elif g=='t':
        tv = tmdb.TV(id)
        trailers = list(filter(lambda v: v['type'] == 'Trailer', tv.videos()['results']))
        teasers = list(filter(lambda v: v['type'] == 'Teaser', tv.videos()['results']))
        frontend = {
            "info": tv.info(),
            "cast": tv.credits()['cast'][:15],
            "crew": tv.credits()['crew'][:15],
            "trailers": trailers,
            "teasers": teasers,
            "alt": tv.alternative_titles()
        }
    return render(request, "details.html", frontend)

def movie(request):
    
    query = str(request.GET.get('query', ''))
   
    upcoming_movie_tmdb = tmdb.Movies('upcoming')
    upcoming_movie = upcoming_movie_tmdb.info()['results']
    now_playing_movie_tmdb = tmdb.Movies('now_playing')
    now_playing_movie = now_playing_movie_tmdb.info()['results']
    popular_movie_tmdb = tmdb.Movies('popular')
    popular_movie = popular_movie_tmdb.info()['results']
    top_rated_movie_tmdb = tmdb.Movies('top_rated')
    top_rated_movie = top_rated_movie_tmdb.info()['results']
  

    return render(request, "movie_page.html", { 'upcoming_movie':upcoming_movie ,'popular_movie':popular_movie, 'top_rated_movie':top_rated_movie,'now_playing_movie':now_playing_movie})

def series(request):
    
    query = str(request.GET.get('query', ''))
    airing_today_series_tmdb = tmdb.TV('airing_today')
    airing_today_series = airing_today_series_tmdb.info()['results']
    on_the_air_series_tmdb = tmdb.TV('on_the_air')
    on_the_air_series = on_the_air_series_tmdb.info()['results']
    popular_series_tmdb = tmdb.TV('popular')
    popular_series = popular_series_tmdb.info()['results']
    top_rated_series_tmdb = tmdb.TV('top_rated')
    top_rated_series = top_rated_series_tmdb.info()['results']

    

    return render(request, "series_page.html", {'airing_today_series':airing_today_series ,'popular_series':popular_series, 'top_rated_series':top_rated_series,'on_the_air_series': on_the_air_series})































def login_view(request):
    login_form = LoginForm(request.POST or None)
    context = {}
    if request.method == 'POST':
        if login_form.is_valid():

            username = login_form.cleaned_data.get('username')
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                login(request, user)

                return redirect('home')
            
    context['form'] = login_form
    
    return render(request, 'log-in.html', context=context)
        
             


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password, email=email)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'sign-up.html', {'form': form})
    
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signup')
        
  
