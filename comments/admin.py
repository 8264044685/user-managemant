from django.contrib import admin
from comments.models import post
from comments.models import comment

# Register your models here.
class posts(admin.ModelAdmin):
    list_display = ['id','content','image','comments']

class comments(admin.ModelAdmin):
    list_display = ['comment_id','messages','no_of_like']
    list_editable = ['messages',]
    list_per_page = 10

admin.site.register(post,posts)
admin.site.register(comment,comments)



