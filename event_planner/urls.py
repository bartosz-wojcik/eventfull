"""event_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from website_pages.views import *
from django.contrib.staticfiles.views import serve as serve_static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='base.html')),
    path('change_password/', auth_views.PasswordChangeForm),
    path('signup/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('advanced_search/', advanced_search, name='advanced_search'),
    path('like_event', like_event, name='like_event'),
    path('unlike_event', unlike_event, name='unlike_event'),
    path('change_password', change_password),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edited_profile/', edited_profile, name='edited_profile'),
    path('delete_profile/<int:id>', delete_profile, name='delete_profile'),
    path('deleted_profile', deleted_profile, name='deleted_profile'),
    path('notifications', notifications, name='notifications'),
    path('promoter/', promoter, name='promoter'),
    path('create_event/', create_event, name='create_event'),
    path('created_event/', created_event, name='created_event'),
    path('promoter_view', promoter_view, name='promoter_view'),
    path('delete_event/<int:id>', delete_event, name='delete_event'),
    path('deleted_event/', deleted_event, name='deleted_event'),
    path('edit_event/<int:id>/', edit_event, name='edit_event'),
    path('edited_event/', edited_event, name='edited_event'),
    path('create_promotion/', create_promotion, name= 'create_promotion'),
    path('created_promotion/', created_promotion, name= 'created_promotion'),
    path('view_promotion/', view_promotions, name='view_promotion'),
    path('edit_promotion/<int:id>/', edit_promotions, name='edit_promotion'),
    path('edited_promotion/', edited_promotions, name='edited_promotion'),
    path('delete_promotion/<int:id>', delete_promotion, name="delete_promotion"),
    path('deleted_promotion/', deleted_promotion, name="deleted_promotion"),
]


# butler used to server files on server
def _static_butler(request, path, **kwargs):
    return serve_static(request, path, insecure=True, **kwargs)

# if not in debug mode, add path to static files
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'static/(.+)', _static_butler)
    ]


