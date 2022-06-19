from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Player, Message
from django.contrib.auth import logout
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('accounts:chat')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('accounts:chat')

def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('accounts:chat')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': Player.objects.exclude(username=request.user.username)})

def message_view(request, sender, receiver): 
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': Player.objects.exclude(username=request.user.username), #List of users
                       'receiver': Player.objects.get(id=receiver), # Receiver context user object for using in template
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)}) #


def logout_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:chat')
    logout(request)
    return redirect('accounts:index')