from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
                  re_path(r'^create_post?/$', views.create_post, name='create_post'),
                  path('Show_user_post', views.Show_user_post, name='Show_user_post'),
                  path('user_comment', views.user_comment, name='user_comment'),
                  path('show_post_comment', views.show_post_comment, name='show_post_comment'),
                  path('comment_like', views.comment_like, name='comment_like'),
                  path('like_show', views.like_show, name='like_show')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
