from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
# advanced
from django.views import generic

from .models import Book, BookInstance, Author
from .models import Question

from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    lastest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        'latest_question_list': lastest_question_list,
    }
    return render(request, template_name='catalog/index.html', context=context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exists")
    return render(request, template_name='catalog/detail.html', context={'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

@login_required
def index_example(request):
    num_books = Book.objects.all().count()
    num_books_instance = BookInstance.objects.all().count()

    num_instance_avaiable = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.all().count()

    # sessions
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_books_instance': num_books_instance,
        'num_instance_avaiable': num_instance_avaiable,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    return render(request, 'example/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    template_name = 'example/book_list.html'

    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


# two method to display detail page
"""
    Có 2 cách để hiển thị 
    cách 1 : tốn bộ nhớ và dung lượng khi mỗi lần đều phải query 
    cách 2 : class không nên 
"""


def book_detail_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'example/book_detail.html', context={'book': book})


"""
    làm cái author 
"""


def index_author(request):
    author_list = Author.objects.all()
    content = {
        'author_list': author_list
    }
    return render(request, 'example/author_list.html', context=content)


def author_detail_view(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        raise Http404('Author does not exist')

    return render(request, 'example/author_detail.html', context={'author': author})
