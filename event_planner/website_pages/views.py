from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def welcome(request):
    return HttpResponse("Welcome to Eventfull! Hamiltons ON-GOING events."
                        " All events cancelled due to Coronavirus public safety measures")

def advanced_search(request):
    return HttpResponse("Perform an advanced search on ")

def register(request):
    return HttpResponse("Register your account for more Eventfull features!")

def login(request):
    return HttpResponse("Log into your account!")

def password_recovery(request):
    return HttpResponse("Recover your password!")

def change_password(request):
    return HttpResponse("Change your password!")

def user_logged_in(request):
    return HttpResponse("View in more ways!")

def edit_profile(request):
    return HttpResponse("Edit your profile!")

def delete_profile(request):
    return HttpResponse("Delete your profile!")

def notifications(request):
    return HttpResponse("See your notifcations!")

def purchase_tickets(request):
    return HttpResponse("Purchase your tickets!")

def checkout(request):
    return HttpResponse("See your notifcations!")

def promoter(request):
    return HttpResponse("Promoter has logged in!")

def create_event(request):
    return HttpResponse("Create an event!")

def view_events(request):
    return HttpResponse("View your events!")

def delete_event(request):
    return HttpResponse("Delete an event!")

def update_event(request):
    return HttpResponse("Update an event!")

def create_promotion(request):
    return HttpResponse("Create a promotion!")

def view_promotions(request):
    return HttpResponse("View promotions!")

def delete_promotion(request):
    return HttpResponse("View promotions!")

def update_promotion(request):
    return HttpResponse("View promotions!")

def view_reports(request):
    return HttpResponse("View promotions!")


