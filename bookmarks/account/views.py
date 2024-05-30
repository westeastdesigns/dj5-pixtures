from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile

# retrieve the Django User model dynamically
User = get_user_model()


# These classes define the views for the account application
def user_login(request):
    """user_login is used to authenticate users against the database. It's a basic
    function-based login view. When called with a GET request, a new login form is
    instantiated and passed to the template. When called with a POST request

    Args:
        request(GET): a login form will be passed to the template
        request(POST): a login form will be passed to the template, then validated.
        If it is invalid, an error appears. If valid, the user is authenticated against
        the database, taking the request object, username, and password parameters. If
        authenticated, it returns the User object. If not, it returns None and sends a
        raw HttpResponse with an invalid login message. Authenticated users are checked
        for active status, if inactive the HttpResponse returns the disabled account
        message. If the authenticated user is active they are set in the session and an
        authenticated successully message is returned as the HttpResponse.

    Returns:
        form (LoginForm): log in form passed to template
        response (HttpResponse): displays the response to the request to the user
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    """dashboard funtion-based view displays a dashboard when users log into their
    account. If authenticated, the user gets the decorated view. If not, user is
    redirected to the login URL, with their requested URL as GET parameter 'next'.

    Returns:
        HttpResponse: account/dashboard.html
        dict: section, dashboard
    """
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    """register is a function-based view for creating user accounts. Hashing is done
    with set_password() of the user model.

    Args:
        request (POST): user_form

    Returns:
        HttpResponse: account/register_done.html or account/register.html
        dict: new_user or user_form
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            # Create user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                "account/register_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    """edit lets logged-in users edit their profile.

    Args:
        request (UserEditForm): stores data of the built-in user model
        request (ProfileEditForm): stores data in the custom Profile model

    Returns:
        form data: if data is validated, it is saved in the respective form
    """
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request):
    """user_list is a simple list view for active User objects

    Args:
        request (User model): gets all User objects

    Returns:
        HttpResponse: sends a list of all active User objects
    """
    users = User.objects.filter(is_active=True)
    return render(
        request, "account/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request, username):
    """user_detail is a detail view for User objects.

    Args:
        request (User model): check User objects
        username (string): used to retrieve the active user with the given username

    Returns:
        HttpResponse: 404 if no active user with the given username is found
    """
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "account/user/detail.html", {"section": "people", "user": user}
    )
