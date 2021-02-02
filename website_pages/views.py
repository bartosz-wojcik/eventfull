
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from website_pages.forms import CustomUserCreationForm
from website_pages.models import Event, UserProfile, Category, Promotion
from django.db.models import Case, When


# Create your views here.

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

    if request.method == 'POST' and request.POST["type"] == 'advanced':

        event_name = request.POST["event-name"]
        venue_name = request.POST["venue-name"]
        event_type = request.POST["event-type"]
        category = request.POST["category-name"]
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]

        events = Event.objects.filter(
            name__icontains=event_name)
        events.filter(
            venue_name__icontains=venue_name).filter(
            category=Category.objects.filter(name=category)).filter(
            start_date=start_date).filter(
            end_date=end_date).filter(
            event_type=event_type)

        return render(request, 'base.html', {'events': events, 'type': 'user'})

    elif request.user.is_authenticated and request.method == 'POST' and request.POST["type"] == 'searche':
        query = request.POST.get('event-name', None)
        events = Event.objects.filter(name__icontains=query)
        return render(request, 'base.html', {'events': events, 'type': 'user'})

    elif request.user.is_authenticated:
        username = request.user
        query = UserProfile.objects.get(id=username.id)

        if query.user_type == "p":
            return render(request, 'promoter.html')

        if query.user_type == "u":
            events = Event.objects.all()
            return render(request, 'base.html', {'events': events, 'type': 'user'})

    else:
        if request.method == 'POST':
            query = request.POST.get('event-name', None)
            events = Event.objects.filter(name__icontains=query)
            return render(request, 'base.html', {'events': events, 'type': 'user'})
        else:
            events = Event.objects.all()
            return render(request, 'base.html', {'events': events, 'type': 'user'})



def advanced_search(request):

    categories = Category.objects.all()
    return render(request, 'advanced_search.html', {'categories': categories})


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
        event_type = request.POST["event-type"]
        category = request.POST["category-name"]
        description = request.POST["description"]
        venue_name = request.POST["venue-name"]
        performer_names = request.POST["performer-names"]
        ticket_price = request.POST["ticket-price"]
        ticket_quantity = request.POST["ticket-quantity"]
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]
        category = Category.objects.get(name=category)

        if event_type == 'f':
            create = Event(
                name=event_name,
                description=description,
                promoter=UserProfile.objects.get(id=username.id),
                category=Category.objects.get(id=category.id),
                venue_name=venue_name,
                event_type=event_type,
                performer_names=performer_names,
                ticket_price=0.00,
                ticket_quantity=0,
                start_date=start_date,
                end_date=end_date)
            create.save()
        else:
            create = Event(
                name=event_name,
                description=description,
                promoter=UserProfile.objects.get(id=username.id),
                category=Category.objects.get(id=category.id),
                venue_name=venue_name,
                event_type=event_type,
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
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]

        # update the event
        update = Event.objects.get(id=id)
        update.name = event_name
        update.description = description
        update.venue_name = venue_name
        update.performer_names = performer_names
        update.ticket_price = ticket_price
        update.start_date = start_date
        update.end_date = end_date
        update.save()

    return redirect('home')

def delete_promotion(request, id):
    promotion = Promotion.objects.filter(id=id)
    return render(request, 'delete_promotion.html', {'promotion': promotion})

def deleted_promotion(request):
    if request.method == 'POST':
        id = request.POST["pk"]
        Promotion.objects.filter(id=id).delete()
    return redirect('home')


def create_promotion(request):
    username = request.user
    events = Event.objects.filter(promoter=username.id)
    return render(request, 'create_promotion.html', {'events': events})

def created_promotion(request):

    if request.method == 'POST':
        username = request.user

        event_name = request.POST["event-name"]
        description = request.POST["description"]
        promotion_code = request.POST["promotion-code"]
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]

        event = Event.objects.get(name=event_name)
        print(event.id)

        create = Promotion(
            promo_code=promotion_code,
            description=description,
            promoter = UserProfile.objects.get(id=username.id),
            event=Event.objects.get(id=event.id),
            start_date=start_date,
            end_date=end_date)

        create.save()

    return redirect('home')

def view_promotions(request):

    if request.user.is_authenticated:
        username = request.user
        id = username.id
        promotions = Promotion.objects.filter(promoter_id=id)
        return render(request, 'view_promotion.html', {'promotions': promotions})

def edit_promotions(request, id):
    promotions = Promotion.objects.filter(id=id)
    return render(request, 'edit_promotion.html', {'promotions': promotions})

def edited_promotions(request):
    if request.method == 'POST':
        id = request.POST["pk"]
        description = request.POST["description"]
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]

        # update the event
        update = Promotion.objects.get(id=id)
        update.description = description
        update.end_date = end_date
        update.start_date = start_date
        update.save()

        return redirect('home')

def view_reports(request):
    return HttpResponse("View promotions!")


