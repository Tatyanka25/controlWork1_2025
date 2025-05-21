from django.urls import path

from movie_app import views

urlpatterns = [
    
    path('show_all/', views.show_all, name='show_all'),
    path('show_one/<int:id>/', views.show_one, name='show_one'),
]
