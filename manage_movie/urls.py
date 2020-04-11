# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url,include
from manage_movie import views
urlpatterns = [
    # url(r'admin/', admin.site.urls),
    url(r'movie/list/$', views.MovieList.as_view(), name='movie_list'),
    url(r'movie/add/$', views.Movie.as_view(), name='movie_add'),
    url(r'movie/search/$', views.SearchMovie.as_view(), name='movie_search'),
    url(r'movie/edit/(?P<pk>[0-9]+)$', views.MovieList.as_view(), name='movie_edit'),
]
