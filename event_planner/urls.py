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
from django.urls import include,path
from django.contrib.auth import views as auth_views
from website_pages.views import *
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='base.html')),
    path('signup/', register, name='register'),
    path('advanced_search/', advanced_search, name='advanced_search'),
    path('password_recovery', password_recovery),
    path('change_password', change_password),
    path('edit_profile', edit_profile),
    path('delete_profile', delete_profile),
    path('notifications', notifications),
    path('purchase_tickets', purchase_tickets),
    path('checkout', checkout),
    path('promoter/', promoter, name='promoter'),
    path('create_event/', create_event, name='create_event'),
    path('created_event/', created_event, name='created_event'),
    path('promoter_view', promoter_view),
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
    path('view_reports', view_reports)
]



