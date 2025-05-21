#from django.contrib import admin
from django.urls import path

from . import views

app_name = "myApp1"
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('hello/', views.hello, name='hello'),
    path('hello2/', views.hello2, name='hello2'),
    path('signs_2/<str:sign>', views.signs_2, name='signs.2'),
    path('calc/<str:str_value>', views.calc),
    path('get_signs/<int:sign>', views.get_sign_info_by_num),
    path('get_signs/<str:sign>', views.get_sign_info),
    path('signs_3/', views.signs_3, name='signs.3'),
    path('get_signs_by_num/<int:sign>', views.get_sign_info_by_num_2, name='get_sign_info_by_num_2'),
    path('get_sign_one/<int:sign>', views.get_sign_one, name='get_sign_one'),
    path('show_all/', views.show_all, name='show_all'),
]