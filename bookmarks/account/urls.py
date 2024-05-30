from django.urls import include, path

from . import views

urlpatterns = [
    # previous login url
    # path("login/", views.user_login, name="login"),
    # login / logout urls
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # change password urls
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(),
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # # reset password urls
    # path(
    #     "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    # Django's authentication url patterns
    path("", include("django.contrib.auth.urls")),
    # user dashboard url
    path("", views.dashboard, name="dashboard"),
    # user registration url
    path("register/", views.register, name="register"),
    # url for user profile editing
    path("edit/", views.edit, name="edit"),
    # url for list of active users
    path("users/", views.user_list, name="user_list"),
    # url for details about a particular user
    path("users/<username>/", views.user_detail, name="user_detail"),
]
