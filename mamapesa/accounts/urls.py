from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.user_registration, name='register'),
    path('login/',views.LoginWithToken.as_view(),name="login"),
    path('logout/',views.LogoutView.as_view(),name="logout"),
    path('password-reset/',views.PasswordReset.as_view(),name="password-reset"),
    path('account-activation/<str:uid>/<str:token>/',views.AccountActivation,name="account-activation"),
]

