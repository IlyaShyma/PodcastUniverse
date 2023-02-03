from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Podcast)
admin.site.register(Episode)
admin.site.register(Comment)
admin.site.register(Invitation)
