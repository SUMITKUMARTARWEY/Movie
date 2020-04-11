from django.shortcuts import render,redirect
import requests
from rest_framework.views import APIView
from manage_movie.models import ManageMovie
from django.db.models import Q
# print(Movie)
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def movie_api(dict_key):
    apikey={}
    apikey['apikey']="2360db30"
    apikey['type']="movie"
    apikey.update(dict_key)
    PARAMS=apikey
    URL = "http://www.omdbapi.com/" 
    r = requests.get(url = URL, params = PARAMS) 
    return r.json()


class Movie(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'movie_add.html'
    def get(self, request,format=None):

       return render(request,self.template_name,{})

    def post(self,request,format=None):
        title=(request.POST['title']).strip()
        # print(title)
        movie_data=movie_api({'t':title})
        # print(movie_data['Response'])
        if(movie_data['Response']=="True"):  
            movie_create=ManageMovie.objects.create(title=movie_data['Title'],genre=movie_data['Genre'],director=movie_data['Director'],writer=movie_data['Writer'],plot=movie_data['Plot'],poster=movie_data['Poster'],imdb_id=movie_data['imdbID'],realease_date=movie_data['Released'],imdb_rating=movie_data['imdbRating'],actor=movie_data['Actors'])
            return redirect("movie_list")
        else:
            error_msg="No Movie available with this name"
            return render(request,self.template_name,{"error":error_msg})  

class MovieList(APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name="index.html"

    def get(self,request,pk=None,format=None):
        # print(pk)
        movie=ManageMovie.objects.all()
        search=self.request.query_params.get('search','')
        page  = self.request.query_params.get('page',1)

        # pk=self.get_object(pk)
        # print(movie_object)
        if pk is not None:
            movie_object=ManageMovie.objects.get(id=pk)
            return render(request,"movie_edit.html",{"movie_data":movie_object})
        if len(search)>0:
            movie=movie.filter(Q(title__icontains=search)|Q(genre__icontains=search)|Q(director__icontains=search)|Q(writer__icontains=search)|Q(plot__icontains=search)|Q(imdb_rating__icontains=search)|Q(actor__icontains=search))
        paginator = Paginator(movie, 10)
        try:
            movie_object = paginator.page(page)
        except PageNotAnInteger:
            movie_object = paginator.page(1)
        except EmptyPage:
            movie_object = paginator.page(paginator.num_pages)
        return render(request,self.template_name,{"movie_data":movie_object,"search":search,"total_records":movie.count()})

        # pass
    def post(self, request, pk, format=None):
        # pk = self.get_object(pk)
        movie_object=ManageMovie.objects.filter(id=pk).update(genre=request.POST['genre'],director=request.POST['director'],writer=request.POST['writer'],plot=request.POST['plot'],actor=request.POST['actor'])
        return redirect("movie_list")


class SearchMovie(APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name="search_movie.html"

    def get(self,request):
        search_movie=self.request.query_params.get('search','')
        movie_data={}
        if len(search_movie)>0:
            movie_data=movie_api({"s":search_movie})
            movie_data=movie_data['Search']
        return render(request,self.template_name,{"movie_data":movie_data,"search":search_movie})
            
