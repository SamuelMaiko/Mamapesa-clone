from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.LoginWithToken.as_view(),name="login"),
    path('testing/',views.TestView.as_view(),name="testing"),
]
