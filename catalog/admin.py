from django.contrib import admin

# Register your models here.
from .models import Question

admin.site.register(Question) # đăng ký bảng question lên admin để quản lý
