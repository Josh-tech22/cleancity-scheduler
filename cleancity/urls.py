from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from scheduling import views as user_views

admin.site.site_header = "CleanCity PHC Portal"
admin.site.site_title = "CleanCity Admin"
admin.site.index_title = "Welcome to CleanCity Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scheduling.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='scheduling/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', user_views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)