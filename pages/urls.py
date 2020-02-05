from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name= 'index'),
    path('welcome',views.welcome,name= 'welcome'),
    path('show_data',views.show_data,name= 'show_data'),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

