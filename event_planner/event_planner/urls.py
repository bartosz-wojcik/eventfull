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
from django.urls import path
from django.contrib.auth import views as auth_views

from website_pages.views import welcome
from website_pages.views import advanced_search
from website_pages.views import register
from website_pages.views import password_recovery
from website_pages.views import user_logged_in
from website_pages.views import edit_profile
from website_pages.views import delete_profile
from website_pages.views import notifications
from website_pages.views import purchase_tickets
from website_pages.views import checkout
from website_pages.views import promoter
from website_pages.views import create_event
from website_pages.views import view_events
from website_pages.views import delete_event
from website_pages.views import update_event
from website_pages.views import create_promotion
from website_pages.views import view_promotions
from website_pages.views import view_reports
from website_pages.views import delete_promotion
from website_pages.views import update_promotion
from website_pages.views import change_password


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('advanced_search', advanced_search),
    path('register', register),
    path('register', register),
    path('password_recovery', password_recovery),
    path('change_password', change_password),
    path('user_logged_in', user_logged_in),
    path('edit_profile', edit_profile),
    path('delete_profile', delete_profile),
    path('notifications', notifications),
    path('purchase_tickets', purchase_tickets),
    path('checkout', checkout),
    path('promoter', promoter),
    path('create_event', create_event),
    path('view_events', view_events),
    path('delete_event', delete_event),
    path('update_event', update_event),
    path('create_promotion', create_promotion),
    path('view_promotions', view_promotions),
    path('delete_promotion', delete_promotion),
    path('update_promotion', update_promotion),
    path('view_reports', view_reports),

]



