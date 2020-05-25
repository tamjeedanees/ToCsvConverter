from django.contrib import admin
from .models import Files,Contact
# Register your models here.

admin.site.site_header = "File-Converter Admin"
admin.site.site_title = "File-Converter Admin Portal"
admin.site.index_title = "Welcome to File-Converter Portal"

admin.site.register(Files)
admin.site.register(Contact)