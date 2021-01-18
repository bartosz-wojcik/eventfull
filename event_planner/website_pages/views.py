
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout
from django.shortcuts import render, redirect
from website_pages.forms import CustomUserCreationForm
from website_pages.models import Event, UserProfile



# Create your views here.

# # login user
# def login(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             dj_login(request, user)
#             print("heya")
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'login.html', {'form': form})

# user registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dj_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    # print(UserProfile.objects.get(user_type="user"))
    if UserProfile.user_type == "promoter":

        if request.method == 'POST':
            return render(request, 'promoter.html')
    else:
        if request.method == 'POST':
            query = request.POST.get('event-name', None)
            events = Event.objects.filter(name=query)
        else:
            events = Event.objects.all()
        return render(request, 'base.html', {'events': events})



def advanced_search(request):
    return HttpResponse("Perform an advanced search on ")


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


