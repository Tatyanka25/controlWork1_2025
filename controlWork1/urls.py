#from django.contrib import admin
from django.urls import path

from . import views

app_name = "controlWork1"

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page2/<str:str_value>/<str:city_value>/', views.page2, name='page2_with_data'),
    path('page3/', views.page3, name='page3'),
    path('page4/', views.page4, name='page4'),
    path('page5/', views.page5, name='page5'),
    path('page6/', views.page6, name='page6'),
    path('page1_exhibition/<int:exhibition_id>', views.page1_exhibition, name='page1_exhibition'),
    path('page1_show/<int:show_id>', views.page1_show, name='page1_show'),
    path('order/', views.create_order_view, name='create_order'),
    path('calculate-artwork-cost/', views.calculate_artwork_cost_view, name='calculate_artwork_cost'),
    path('all_calculations_view/', views.all_calculations_view, name='all_calculations_view'),
]
