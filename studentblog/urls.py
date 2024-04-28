from django.contrib import admin
from django.urls import path
from blog import views as blog_views
from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_views.home, name='home'),
    path('category/<slug:category_slug>/', blog_views.home, name='category_home'),
    path('create_post/', blog_views.create_post, name='create_post'),
    path('post_details/title/<slug:post_slug>/usn/<usn>/', blog_views.post_details, name='post_details'),
    path('update_post/<int:post_id>', blog_views.update_post, name='update_post'),
    path('delete_post/<int:post_id>', blog_views.delete_post, name='delete_post'),
    path('delete_comment/<int:post_id>/<int:comment_id>', blog_views.delete_comment, name='delete_comment'),
    path('add_comment/<int:post_id>', blog_views.add_comment, name='add_comment'),
    path('delete_reply/<int:post_id>/<int:reply_id>', blog_views.delete_reply, name='delete_reply'),
    path('add_reply/<int:post_id>/<int:comment_id>', blog_views.add_reply, name='add_reply'),
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.user_logout, name='logout'),
    path('profile/usn/<usn>/', user_views.profile, name='profile'),
    path('profile/<int:author_id>/', user_views.profile, name='author_profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
