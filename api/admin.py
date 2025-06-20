from django.contrib import admin

from .models import Meal,Rating
class RatingAdmin(admin.ModelAdmin):
    list_display=['id','meal','user','stars']
    list_filter=['meal','user']

class MealAdmin(admin.ModelAdmin):
    list_display=['id','title']
    search_fields=['title']
    list_filter=['title','description'] 
    
admin.site.register(Meal,MealAdmin)#to connect the two classes together
admin.site.register(Rating,RatingAdmin)#to connect the two classes together 