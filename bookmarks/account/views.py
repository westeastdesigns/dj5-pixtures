from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


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
