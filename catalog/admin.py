from django.contrib import admin

from .models import Book, Genre, BookInstance, Language, Author
# Register your models here.
from .models import Question

admin.site.register(Question)  # đăng ký bảng question lên admin để quản lý

# admin.site.register(Book)

admin.site.register(Genre)

admin.site.register(BookInstance)

admin.site.register(Language)


# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_date')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
