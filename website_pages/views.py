
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from website_pages.forms import CustomUserCreationForm
from website_pages.models import Event, UserProfile, Category, Promotion, WishList

# Create your views here.


def register(request):
    """
    This function allows the user to register an account
    if form is valid, create a user
    :param request: used for user information and retrieving parameters
    :return: render signup.html and the form fields
    """

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # if the form input is valid
        if form.is_valid():
            # save the form
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # log in user and return to home
            dj_login(request, user)
            return redirect('home')
    else:
        # else send user creation form
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    """
    this function handles user interaction on the home page
    :param request: used for user information and retrieving parameters
    :return: advanced search results, search results, redirect promoter to promoter page, redirect user to home page
    """
    if request.method == 'POST' and 'type' in request.POST:
        # if type is equal to advanced
        # retrieve all events and if parameters are present, filter those parameters in the events query
        if request.POST["type"] == 'advanced':

            events = Event.objects.all()

            if 'event-name' in request.POST and request.POST['event-name'] != "":

                events = events.filter(name__icontains=request.POST['event-name'])

            if 'venue-name' in request.POST and request.POST['venue-name'] != "":
                events = events.filter(venue_name__icontains=request.POST['venue-name'])

            if 'event-type' in request.POST and request.POST['event-type'] != "":
                events = events.filter(event_type=request.POST['event-type'])

            if 'category-name' in request.POST and len(events) > 0:
                category = Category.objects.get(name=request.POST['category-name'])
                events = events.filter(category_id=category.id)

            if 'start-date' in request.POST and request.POST['start-date'] != "":
                events = events.filter(start_date=request.POST['start-date'])

            if 'end-date' in request.POST and request.POST['end-date'] != "":
                events = events.filter(end_date=request.POST['end-date'])

            return render(request, 'base.html', {'events': events, 'type': 'user'})

        # if user is authenticated and performs a search, filter name of event from events query
        # and show filtered events to user
        elif request.user.is_authenticated and request.POST["type"] == 'search':
            query = request.POST.get('event-name', None)
            events = Event.objects.filter(name__icontains=query)
            return render(request, 'base.html', {'events': events, 'type': 'user'})

    # if user is authenticated
    elif request.user.is_authenticated:
        user = request.user
        query = UserProfile.objects.get(id=user.id)
        # if they are promoter, redirect them to promoter page
        if query.user_type == "p":
            return render(request, 'promoter.html')
        # if they are a user, get all events, filter out events in their wish list and display page
        # with events not yet liked
        if query.user_type == "u":

            events = Event.objects.all()
            wishlist = WishList.objects.filter(user_id=user.id)
            for item in wishlist:
                events = events.exclude(name=item.event.name)

            return render(request, 'base.html', {'events': events, 'wishlist': wishlist, 'type': 'user'})
    # else they are a unregistered user
    else:
        if request.method == 'POST':
            # performed a search, filter name of event from events query and show filtered events to user
            query = request.POST.get('event-name', None)
            events = Event.objects.filter(name__icontains=query)
            return render(request, 'base.html', {'events': events, 'type': 'user'})
        else:
            # else show all events in database
            events = Event.objects.all()
            return render(request, 'base.html', {'events': events, 'type': 'user'})




def advanced_search(request):
    """

    :param request:
    :return:
    """
    categories = Category.objects.all()
    return render(request, 'advanced_search.html', {'categories': categories})


def profile(request):

    user = request.user
    wishlist = WishList.objects.filter(user_id=user.id)

    return render(request, 'profile.html', {'wishlist': wishlist})

def like_event(request):

    if request.method == 'GET':

        event_id = request.GET["id"]
        user = request.user

        wishlist = WishList(
            user=UserProfile.objects.get(id=user.id),
            event=Event.objects.get(id=event_id)
        )
        wishlist.save()

        return HttpResponse("liked")

def unlike_event(request):

    if request.method == 'GET':
        event_id = request.GET["id"]

        WishList.objects.filter(
            user_id=UserProfile.objects.get(id=request.user.id),
            event_id=Event.objects.get(id=event_id)
        ).delete()

    return HttpResponse("unliked")


def password_recovery(request):

    return HttpResponse("password")

def change_password(request):
    return HttpResponse("Change your password!")

def user_logged_in(request):

    return HttpResponse("View in more ways!")

def edit_profile(request):
    return render(request, 'edit_profile.html')

def edited_profile(request):
    """
    this functions edits the users profiles - first name, last name and email
    if the paramters are passed, they will be updated

    :param request:
    :return:  user is redirected back to profile
    """

    if request.method == 'POST':
        update = UserProfile.objects.get(id=request.user.id)
        if 'first-name' in request.POST and request.POST['first-name'] != "":
            update.first_name = request.POST['first-name']

        if 'last-name' in request.POST and request.POST['last-name'] != "":
            update.first_name = request.POST['last-name']

        if 'email' in request.POST and request.POST['email'] != "":
            update.first_name = request.POST['email']

        update.save()

    return redirect('profile')

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

    if promotions.promoter_id == request.user.id:
        return render(request, 'edit_promotion.html', {'promotions': promotions})
    else:
        return redirect('home')

def edited_promotions(request):
    if request.method == 'POST':
        id = request.POST["pk"]
        description = request.POST["description"]
        start_date = request.POST["start-date"]
        end_date = request.POST["end-date"]

        update = Promotion.objects.get(id=id)
        #update promotion parameters
        update.description = description
        update.end_date = end_date
        update.start_date = start_date
        update.save()

        return redirect('home')

def view_reports(request):
    return HttpResponse("View promotions!")


