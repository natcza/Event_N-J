"""eventnj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from events.views import (
    DashboardView,
    # EventDetailsView,
    SendMailView,
    EventDetailsView_,
    ParticipantAddView2,
    AuthenticateParticipantView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name="dashboard"),
    path('event-details/<int:pk>/', EventDetailsView_.as_view(), name="event-details"),
    # path('add-participant/<int:pk>', ParticipantAddView.as_view(), name="add-participant"),
    path('add-participant/<int:pk>/', ParticipantAddView2.as_view(), name="add-participant"),

    # https://docs.djangoproject.com/en/4.0/topics/http/urls/#path-converters
    path('authenticate-participant/<uuid:authenticate_code>/', AuthenticateParticipantView.as_view(), name="authenticate-participant"),
    path('send-mail/<int:pk>/', SendMailView.as_view(), name='send-mail'),
]
