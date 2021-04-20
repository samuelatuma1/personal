from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Categories)
class adminCategory(admin.ModelAdmin):
	display_list = ['name']

@admin.register(Product)
class adminCategory(admin.ModelAdmin):
	list_display = ['name', 'category', 'price', 'image', 'qty']
	list_filter = ['name', 'category', 'price']
	ordering = ['-uploaded']
	#raw_id_fields = ['category']
	
admin.site.register(Star)
admin.site.register(UserProfile)
	
	
