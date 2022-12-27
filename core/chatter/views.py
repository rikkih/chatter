from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from chatter.models import Room


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "chatter/index.html", {"rooms": Room.objects.all()})


def room(request: HttpRequest, room_name: str) -> HttpResponse:
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, "chatter/room.html", {"room": chat_room})
