from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    # ex: /catalog/
    path('', views.index, name='index'),
    # ex: /catalog/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /catalog/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /catalog/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]