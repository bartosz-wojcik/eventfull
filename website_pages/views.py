from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from website_pages.forms import CustomUserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from website_pages.models import Event, UserProfile, Category, Promotion, WishList

"""
The views.py files with rendering pages and performing logic based on user interaction
Each function serves templates and controls the application based off of users actions
"""


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
    :return: advanced search results, search results, redirect promoter to promoter page, redirect user to home
    """
    if request.method == 'POST' and 'type' in request.POST:
        # if type is equal to advanced
        # retrieve all events and if parameters are present, filter those parameters in the events query
        if request.POST["type"] == 'advanced':
            try:

                events = Event.objects.all().order_by('start_date')
                # check to see if paramter exists and is not empty, then filter it in query
                if 'event-name' in request.POST and request.POST['event-name'] != "":

                    events = events.filter(name__icontains=request.POST['event-name'])

                if 'venue-name' in request.POST and request.POST['venue-name'] != "":
                    events = events.filter(venue_name__icontains=request.POST['venue-name'])

                if 'event-type' in request.POST and request.POST['event-type'] != "" and\
                        request.POST['event-type'] != "a":
                    events = events.filter(event_type=request.POST['event-type'])

                if 'category-name' in request.POST and len(events) > 0 and request.POST['category-name'] != "all":
                    category = Category.objects.get(name=request.POST['category-name'])
                    events = events.filter(category_id=category.id)
                # if both start date and end date have a value, check in range for events
                if 'start-date' in request.POST and request.POST['start-date'] != "" and 'end-date' in request.POST and\
                        request.POST['end-date'] != "":
                    events = events.filter(end_date__range=[request.POST['start-date'], request.POST['end-date']])
                # else filter them separate
                else:
                    if 'start-date' in request.POST and request.POST['start-date'] != "":
                        events = events.filter(start_date__date=request.POST['start-date'])

                    if 'end-date' in request.POST and request.POST['end-date'] != "":
                        events = events.filter(end_date__date=request.POST['end-date'])


                if len(events) > 0:
                    return render(request, 'home.html', {'events': events, 'type': 'user'})
                else:
                    message = 'No matching events found.'
                    return render(request, 'home.html', {'message': message})
            except:
                message = 'Something went wrong with search. Try again later.'
                return render(request, 'home.html', {'message': message})

        # if user is authenticated and performs a search, filter name of event from events query
        # and show filtered events to user
        elif request.POST["type"] == 'search':
            try:
                if request.user.is_authenticated:
                    query = UserProfile.objects.get(id=request.user.id)
                    if not query.user_type == "u":
                        return redirect('home')

                query = request.POST.get('event-name', None)
                events = Event.objects.filter(name__icontains=query)
                if len(events) > 0:
                    return render(request, 'home.html', {'events': events, 'type': 'user'})
                else:
                    message = 'No events found'
                    return render(request, 'home.html', {'message': message})
            except:
                message = 'Something went wrong with search. Try again later.'
                return render(request, 'home.html', {'message': message})

    # if user is authenticated
    elif request.user.is_authenticated:
        query = UserProfile.objects.get(id=request.user.id)

        # if they are promoter, redirect them to promoter page
        if query.user_type == "p":
            return render(request, 'promoter.html')
        # if they are a user, get all events, filter out events in their wish list and display page
        # with events not yet liked
        if query.user_type == "u":
            try:
                events = Event.objects.all().order_by('start_date')
                wishlist = WishList.objects.filter(user_id=request.user.id)
                for item in wishlist:
                    events = events.exclude(name=item.event.name)
                if (len(events) > 0):
                    return render(request, 'home.html', {'events': events, 'wishlist': wishlist, 'type': 'user'})
                else:
                    message = 'Events cannot be loaded'
                    return render(request, 'home.html', {'message': message})
            except:
                message = 'Events cannot be loaded'
                return render(request, 'home.html', {'message': message})
    # else they are a unregistered user
    else:
        # else show all events in database
        try:
            events = Event.objects.all().order_by('start_date')
            if len(events) > 0:

                return render(request, 'home.html', {'events': events, 'type': 'user'})
            else:
                message = 'There are currently no events.'
                return render(request, 'home.html', {'message': message})
        except:
            message = 'Events cannot be loaded'
            return render(request, 'home.html', {'message': message})


def advanced_search(request):
    """
    this function renders the advanced search page
    :param request: used for user information and retrieving parameters
    :return: advanced search page along with categories for selection input, else return message
    """
    try:
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "u":
                return redirect('home')

        categories = Category.objects.all().order_by('name')
        if len(categories) > 0:
            return render(request, 'advanced_search.html', {'categories': categories})
        else:
            message = 'Could not load data. Please try again later'
            return render(request, 'advanced_search.html', {'message': message})
    except:
        message = 'There was an issue connecting to the database. Please try again later'
        return render(request, 'advanced_search.html', {'message': message})


def profile(request):
    """
    this function renders the user profile page
    :param request: used for user information and retrieving parameters
    :return: render user profile page and wishlist items if user has any liked events, otherwise show no liked events
    """
    try:
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "u":
                return redirect('home')

            wishlist = WishList.objects.filter(user_id=request.user.id)
            if len(wishlist) > 0:
                return render(request, 'profile.html', {'wishlist': wishlist, 'user_id': request.user.id})
            else:
                message = 'No events in your wishlist'
                return render(request, 'profile.html', {'message': message, 'user_id': request.user.id})
        else:
            return redirect('home')
    except:
        message = 'Error loading the profile page. Try again later.'
        return render(request, 'profile.html', {'message': message})


def like_event(request):
    """
    this function gets an event id and adds that event to the users wishlist
    :param request: used for user information and retrieving parameters
    :return: returns a message upon success or error message if something goes wrong.
    """

    if request.method == 'GET':
        try:
            event_id = request.GET["id"]
            wishlist = WishList(
                user=UserProfile.objects.get(id=request.user.id),
                event=Event.objects.get(id=event_id)
            )
            wishlist.save()
            return HttpResponse("Event has been added to WishList!")
        except:
            message = 'Unable to like Event. Try again later.'
            return render(request, 'home.html', {'message': message})


def unlike_event(request):
    """
    this function gets an event id and removes that event from the users wishlist
    :param request: used for user information and retrieving parameters
    :return: returns a message upon success or error message if something goes wrong.
    """
    if request.method == 'GET':
        try:
            event_id = request.GET["id"]
            WishList.objects.filter(
                user_id=UserProfile.objects.get(id=request.user.id),
                event_id=Event.objects.get(id=event_id)
            ).delete()
            message = "Event has been removed from WishList"
            return HttpResponse({'message': message})
        except:
            message = 'Unable to Unlike Event. Try again later.'
            return render(request, 'home.html', {'message': message})


def change_password(request):
    """
    this function allows the user to change their password. User will be presented a change password page
    Upon updating password, they will remain logged in and be redirected back to their profile
    :param request: used for user information and retrieving parameters
    :return: change password page for user
    """
    try:
        if request.method == 'POST':
            # get create form template with data and usre
            form = PasswordChangeForm(data=request.POST, user=request.user)
            # if the form is filled out correctly
            # save form
            # update session for user
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        # else show password change form to user to fill out
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'change_password.html', {'form': form})
    except:
        return render(request, 'promoter.html', {'form': form})


def edit_profile(request):
    """
    this function renders the edit_profile page for a logged in user
    :param request: used for user information and retrieving parameters
    :return: render edit profile page
    """
    try:
        # check if logged in and user, else redirect home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "u":
                return redirect('home')
        # user information is not sent, they are only allowed to edit f name, l name and email
        return render(request, 'edit_profile.html')
    except:
        message = "Something went wrong while Editing profile. Try again later."
        return render(request, 'profile.html', {'message': message})


def edited_profile(request):
    """
    this functions edits the users profiles - first name, last name and email
    if the paramters are passed, they will be updated in the UserProfile
    :param request: used for user information and retrieving parameters
    :return:  user is redirected back to profile
    """
    if request.method == 'POST':
        try:
            update = UserProfile.objects.get(id=request.user.id)
            if 'first-name' in request.POST and request.POST['first-name'] != "":
                update.first_name = request.POST['first-name']

            if 'last-name' in request.POST and request.POST['last-name'] != "":
                update.first_name = request.POST['last-name']

            if 'email' in request.POST and request.POST['email'] != "":
                update.first_name = request.POST['email']

            update.save()
            return redirect('profile')
        except:
            message = "Something went wrong while updating Profile. Try again later."
            return render(request, 'profile.html', {'message': message})


def delete_profile(request, id):
    """
    this function renders the delete profile page for user
    :param request: used for user information and retrieving parameters
    :param id: the id of user deleting profile
    :return: render delete profile page along with user profile data
    """
    try:
        # if user is logged in and is of type user proceed, else return them home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "u":
                return redirect('home')

            # if user deleting profile is owner of profile
            if request.user.id == id:
                user_profile = UserProfile.objects.get(id=id)
                return render(request, 'delete_profile.html', {'user_profile': user_profile})
            else:
                return redirect('home')
        else:
            return redirect('home')
    except:
        message = "Something went wrong while loading Profile data. Try again later."
        return render(request, 'profile.html', {'message': message})


def deleted_profile(request):
    """
    this function deletes a users profile
    :param request: used for user information and retrieving parameters
    :return: delete profile and return user back to home
    """
    try:
        # if user is logged in and is of type user proceed, else return them home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "u":
                return redirect('home')

        UserProfile.objects.get(id=request.user.id).delete()
        return redirect('home')
    except:
        message = "Something went wrong while deleting Profile. Try again later."
        return render(request, 'home', {'message': message})


def notifications(request):
    """
    this functions shows user promotions available for the events on the users wishlist
    :param request: used for user information and retrieving parameters
    :return: notifications page along with promotions from events in the users wishlist
    """
    try:
        # if user is logged in and is of type user proceed, else return them home
        if request.user.is_authenticated:
            event_id_query = UserProfile.objects.get(id=request.user.id)
            if not event_id_query.user_type == "u":
                return redirect('home')

            # holds events ids
            event_id_query = []
            wishlist = WishList.objects.filter(user_id=request.user.id)
            if len(wishlist) > 0:
                for i in wishlist:
                    event_id_query.append(i.event_id)
            promotions = Promotion.objects.filter(event_id__in=event_id_query)

            if len(promotions) > 0:
                return render(request, 'notifications.html', {'promotions': promotions})
            else:
                message = "No promotions have been found. Like events to see promotions"
                return render(request, 'notifications.html', {'message': message})
    except:
        message = "Something went wrong while retrieving promotions. Try again later."
        return render(request, 'profile.html', {'message': message})


def promoter(request):
    """
     this functions redirects user to promoters page
     :param request: used for user information and retrieving parameters
     :return: redirect to promoter page, if they are a promoter, else send them to home
    """
    # if user is logged in and is of type promoter proceed, else return them home
    try:
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')
        else:
            return redirect('home')
    except:
        message = "Something went wrong while loading the promoter page. Try again later."
        return render(request, 'promoter.html', {'message': message})


def create_event(request):
    """
    this functions renders the create event page for a promoter
    :param request: used for user information and retrieving parameters
    :return:  event create page with categories available for events
    """
    try:
        # if user is logged in and is of type promoter proceed, else return them home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        categories = Category.objects.all()
        return render(request, 'promoter_create.html', {'categories': categories})
    except:
        message = "Something went wrong while creating user"
        return render(request, 'promoter.html', {'message': message})


def created_event(request):
    """
    this function creates an event from user input
    check if free or paid event and create accordingly
    :param request: used for user information and retrieving parameters
    :return: user to home after creating a new event
    """
    try:
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

            # if the event is free
            # apply parameters and create event
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
            # else its a paid event
            # apply parameters and create event
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

        return redirect('promoter_view')
    except:
        message = "Something went wrong while creating event. Try again later."
        return render(request, 'promoter.html', {'message': message})


def promoter_view(request):
    """
    this function renders the event view page for the promoter along with events associated with the promoter
    (sorry for the horrid  template names, im too scared to refactor anything at this point - should be view_events)
    :param request: used for user information and retrieving parameters
    :return:
    """
    try:
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        events = Event.objects.filter(promoter=request.user.id).order_by('start_date')
        if len(events) > 0:
            return render(request, 'promoter_view.html', {'events': events, 'type': 'promoter'})
        else:
            message = "No events are available. Create events to see data"
            return render(request, 'promoter_view.html', {'message': message})
    except:
        message = "Something went wrong while trying to view events. Try again later."
        return render(request, 'promoter.html', {'message': message})


def delete_event(request, id):
    """
    this function rends the delete event page for a promoter
    :param request: used for user information and retrieving parameters
    :param id: id of event to be deleted
    :return: delete page with events of the promoter
    """
    try:
        # check to see if they are promoter, otherwise redirect them to home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        events = Event.objects.filter(id=id)
        return render(request, 'promoter_delete.html', {'events': events, 'type': 'edit'})
    except:
        message = "Something went wrong while trying to load delete events page. Try again later."
        return render(request, 'promoter.html', {'message': message})


def deleted_event(request):
    """
    this function deletes a event from the database
    :param request: used for user information and retrieving parameters
    :return: returns the promoter to home after deleting
    """
    try:
        if request.method == 'POST':
            id = request.POST["pk"]
            Event.objects.filter(id=id).delete()
        return redirect('promoter_view')
    except:
        message = "Something went wrong when trying to delete event. Try again later."
        return render(request, 'promoter.html', {'message': message})


def edit_event(request, id):
    """
    this function renders the edit event page for a promoter, along with event data
    :param request: used for user information and retrieving parameters
    :param id: id of event being edited
    :return: edit event page along with the event being updated
    """
    try:
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        events = Event.objects.filter(id=id)
        return render(request, 'promoter_edit.html', {'events': events, 'type': 'edit'})
    except:
        message = "Something went wrong while loading edit event page. Try again later."
        return render(request, 'promoter.html', {'message': message})

@csrf_protect
def edited_event(request):
    """
    this function edits an event after receiving parameters from user
    :param request: used for user information and retrieving parameters
    :return: update event and send user back home
    """
    try:
        if request.method == 'POST':
            id = request.POST["pk"]
            event_name = request.POST["event-name"]
            description = request.POST["description"]
            venue_name = request.POST["venue-name"]
            performer_names = request.POST["performer-names"]
            ticket_price = request.POST["ticket-price"]
            ticket_quantity = request.POST["ticket-quantity"]
            start_date = request.POST["start-date"]
            end_date = request.POST["end-date"]

            # update the event
            update = Event.objects.get(id=id)
            update.name = event_name
            update.description = description
            update.venue_name = venue_name
            update.performer_names = performer_names
            update.ticket_price = ticket_price
            update.ticket_quantity = ticket_quantity
            update.start_date = start_date
            update.end_date = end_date
            update.save()
        return redirect('promoter_view')
    except:
        message = "Something went wrong while updating the event. Try again later."
        return render(request, 'promoter.html', {'message': message})


def delete_promotion(request, id):
    """
    this function takes the promoter to a delete promotion page with associated event id
    :param request: used for user information and retrieving parameters
    :param id: promotion id to be deleted
    :return: render delete promotion page with promotion data
    """
    try:
        # check to see if they are promoter, otherwise redirect them to home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        promotion = Promotion.objects.filter(id=id)
        return render(request, 'delete_promotion.html', {'promotion': promotion})
    except:
        message = "Something went wrong while loading delete promotion page. Try again later."
        return render(request, 'promoter.html', {'message': message})


def deleted_promotion(request):
    """
    this function deletes a promotion
    :param request: used for user information and retrieving parameters
    :return: delete promotion specified by promoter and return them to home
    """
    try:
        if request.method == 'POST':
            id = request.POST["pk"]
            Promotion.objects.filter(id=id).delete()
        return redirect('view_promotion')
    except:
        message = "Something went wrong while tyring to delete promotion. Try again later."
        return render(request, 'promoter.html', {'message': message})


def create_promotion(request):
    """
    this function takes the promoter to a create promotion page
    :param request: used for user information and retrieving parameters
    :return: render create promotion page along with event data
    """
    try:
        # check to see if they are promoter, otherwise redirect them to home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        events = Event.objects.filter(promoter_id=request.user.id)
        return render(request, 'create_promotion.html', {'events': events})
    except:
        message = "Something went wrong while tyring to load create promotion page. Try again later."
        return render(request, 'promoter.html', {'message': message})


def created_promotion(request):
    """
    this function creates a promotion with parameters passed by the promoter
    :param request: used for user information and retrieving parameters
    :return:
    """
    try:
        if request.method == 'POST':
            username = request.user

            event_name = request.POST["event-name"]
            event_name = event_name.split('-')
            event_id = event_name[-1]
            description = request.POST["description"]
            promotion_code = request.POST["promotion-code"]
            start_date = request.POST["start-date"]
            end_date = request.POST["end-date"]

            event = Event.objects.get(id=event_id)

            create = Promotion(
                promo_code=promotion_code,
                description=description,
                promoter = UserProfile.objects.get(id=username.id),
                event=Event.objects.get(id=event.id),
                start_date=start_date,
                end_date=end_date)

            create.save()

        return redirect('view_promotion')
    except:
        message = "Something went wrong while creating the promotion. Try again later."
        return render(request, 'promoter.html', {'message': message})


def view_promotions(request):
    """
    this function takes the promoter to the view promotions page
    :param request: used for user information and retrieving parameters
    :return: render view promotions page along with promotion data
    """
    try:
        # check to see if they are promoter, otherwise redirect them to home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        promotions = Promotion.objects.filter(promoter_id=request.user.id).order_by('start_date')
        if len(promotions) > 0:
            return render(request, 'view_promotion.html', {'promotions': promotions})
        else:
            message = "There are no promotions to view. Create some promotions!"
            return render(request, 'view_promotion.html', {'message': message})
    except:
        message = "Something went wrong while trying load view promotions page. Try again later."
        return render(request, 'promoter.html', {'message': message})


def edit_promotions(request, id):
    """
    this function takes the promoter to a edit promotions page associated with the promotion id
    :param request: used for user information and retrieving parameters
    :param id: id of the promotion being updated
    :return:
    """
    try:
        # check to see if they are promoter, otherwise redirect them to home
        if request.user.is_authenticated:
            query = UserProfile.objects.get(id=request.user.id)
            if not query.user_type == "p":
                return redirect('home')

        # check to see if promoter is owner of the promotion
        promotions = Promotion.objects.get(id=id)
        # check if promoter is owner of promotion being edited
        if promotions.promoter_id == request.user.id:
            promotions = Promotion.objects.filter(id=id)
            return render(request, 'edit_promotion.html', {'promotions': promotions})
        else:
            return redirect('home')
    except:
        message = "Something went wrong while trying load edit promotions page. Try again later."
        return render(request, 'promoter.html', {'message': message})


def edited_promotions(request):
    """
    this function edits a promotion with paramters passed by promoter
    :param request: used for user information and retrieving parameters
    :return: save edits made to the promotion and send promoter to home
    """
    try:
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

            return redirect('view_promotion')
    except:
        message = "Something went wrong while editing the promotion. Try again later."
        return render(request, 'promoter.html', {'message': message})



