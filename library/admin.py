from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Instance)
admin.site.register(Borrower)
admin.site.register(InstanceBorrower)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)