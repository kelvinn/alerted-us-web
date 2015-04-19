# pylint: disable=E1120
from django.shortcuts import render
from django.views.generic.base import View
from apps.people.models import Location


# Create your views here.


class LocationView(View):

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if request.user.username == username:
            locations = Location.objects.filter(user=request.user)
        else:
            locations = None

        return render(request, 'people/location.html', {'locations': locations})


class SettingsView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'people/settings.html', {'user': user})

