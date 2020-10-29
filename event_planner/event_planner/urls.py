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
from website_pages.views import welcome, advanced_search, register, login, password_recovery, change_password,\
    user_logged_in, edit_profile, delete_profile, notifications, purchase_tickets, checkout, promoter, create_event, \
    view_events, delete_event, update_event, create_promotion, view_promotions, delete_promotion, update_promotion, \
    view_reports


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome),
    path('advanced_search', advanced_search),
    path('register', register),
    path('login', login),
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



