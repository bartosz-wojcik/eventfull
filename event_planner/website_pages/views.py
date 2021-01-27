
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from website_pages.forms import CustomUserCreationForm
from website_pages.models import Event, UserProfile, Category


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

    if request.user.is_authenticated:
        username = request.user
        query = UserProfile.objects.get(username=username)

        if query.user_type == "p":
            return render(request,'promoter.html')

        if query.user_type == "u":
            events = Event.objects.all()
            return render(request, 'base.html', {'events': events, 'type': 'user'})

    else:
        # if request.method == 'POST':
        #     query = request.POST.get('event-name', None)
        #     events = Event.objects.filter(name=query)
        #     return render(request, 'base.html', {'events': events})
        # else:
        events = Event.objects.all()
        return render(request, 'base.html', {'events': events, 'type': 'user'})



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

    if request.user.is_authenticated:
        username = request.user
        query = UserProfile.objects.get(username=username)

        if not query.user_type == "p":
            return redirect('home')
    else:
        return redirect('home')


def create_event(request):

    categories = Category.objects.all()
    return render(request, 'promoter_create.html', {'categories': categories})

def created_event(request):
    if request.method == 'POST':
        username = request.user

        event_name = request.POST["event-name"]
        category = request.POST["category-name"]
        description = request.POST["description"]
        venue_name = request.POST["venue-name"]
        performer_names = request.POST["performer-names"]
        ticket_price = request.POST["ticket-price"]
        ticket_quantity = request.POST["ticket-quantity"]
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]


        category = Category.objects.get(name=category)
        print(category.id)

        create = Event(
            name=event_name,
            description=description,
            promoter = UserProfile.objects.get(id=username.id),
            category=Category.objects.get(id=category.id),
            venue_name=venue_name,
            performer_names=performer_names,
            ticket_price=ticket_price,
            ticket_quantity=ticket_quantity,
            start_date=start_date,
            end_date=end_date)

        create.save()

    return redirect('home')

def promoter_view(request):
    if request.user.is_authenticated:

        username = request.user
        print(username.id)
        query = UserProfile.objects.get(username=username)

        if query.user_type == "p":
            events = Event.objects.filter(promoter=username)
            return render(request, 'promoter_view.html', {'events': events, 'type': 'promoter'})
        else:
            return redirect('home')

def delete_event(request, id):
    events = Event.objects.filter(id=id)
    return render(request, 'promoter_delete.html', {'events': events, 'type': 'edit'})

def deleted_event(request):
    if request.method == 'POST':
        id = request.POST["pk"]
        Event.objects.filter(id=id).delete()
    return redirect('home')

def edit_event(request, id):
    events = Event.objects.filter(id=id)
    return render(request, 'promoter_edit.html', {'events': events, 'type': 'edit'})

@csrf_protect
def edited_event(request):
    if request.method == 'POST':
        id = request.POST["pk"]
        event_name = request.POST["event-name"]
        description = request.POST["description"]
        venue_name = request.POST["venue-name"]
        performer_names = request.POST["performer-names"]
        ticket_price = request.POST["ticket-price"]
        ## DATES ARE KILLING ME AND TIME!!!!!!
        ## FUCK DATE FORMATS IN GENERAL!!
        # start_date = request.POST["start-date"]
        # end_date = request.POST["end-date"]

        # update the event
        update = Event.objects.get(id=id)
        update.name = event_name
        update.description = description
        update.venue_name = venue_name
        update.performer_names = performer_names
        update.ticket_price = ticket_price
        update.save()

    return redirect('home')

def delete_promotion(request):
    if request.method == 'POST':
        id = request.POST["pk"]

    return redirect('home')

def create_promotion(request):
    return HttpResponse("Create a promotion!")

def view_promotions(request):
    return HttpResponse("View promotions!")

def update_promotion(request):
    return HttpResponse("View promotions!")

def view_reports(request):
    return HttpResponse("View promotions!")


