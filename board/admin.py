from django.contrib import admin

# Register your models here.
from .models import Board,Document,Subject,User

admin.site.register(Board)
admin.site.register(Document)
admin.site.register(Subject)
admin.site.register(User)
