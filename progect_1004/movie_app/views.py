from django.shortcuts import render
from movie_app.models import Movie

def show_all(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render (request, "show_all.html", context)

def show_one(request, id:int):
    movie = Movie.objects.get(id=id)
    context = {"movie": movie}
    return render (request, "show_one.html", context)