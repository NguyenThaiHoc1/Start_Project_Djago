from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    # ex: /catalog/example/
    path('example/', views.index_example, name="example2"),
    # ex: /catalog/example/book
    path('example/books/', views.BookListView.as_view(), name='books'),
    # ex: /catalog/example/book/5/
    path('example/books/<int:pk>', views.book_detail_view, name='book-detail'),

    # ex: /catalog/example/authors
    path('example/authors/', views.index_author, name='authors'),
    # ex: /catalog/example/author/5/
    path('example/author/<int:pk>', views.author_detail_view, name='author-detail'),

    # ex: /catalog/
    path('', views.index, name='index'),
    # ex: /catalog/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /catalog/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /catalog/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]