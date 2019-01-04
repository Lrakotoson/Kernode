from django.urls import path
from . import views

urlpatterns = [
    #/search/
    path('', views.index, name='index'),
    #/search/results/
    path('<int:search_id>/', views.results, name='results'),
]
