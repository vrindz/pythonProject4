from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Song
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
# def base(request):
#     return render(request, "base.html")
def index(request):
    allSongs = Song.objects.all().order_by('-last_updated')
    return render(request, template_name="index.html", context={"allSongs": allSongs})
def home(request):
    # return HttpResponse("Home Page")

    return render(request, "home.html")


def search_songs(request):
    template_path = 'search_result.html'

    search_query = request.GET.get('search', None)

    if search_query:
        search_result = Song.objects.filter(
            Q(songName__icontains=search_query) |
            Q(album__albumName__icontains=search_query) |
            Q(album__artist__artistName__icontains=search_query)
        ).distinct()
    else:
        search_result = Song.objects.all()

    context = {'search_result': search_result, 'search_query': search_query}
    return render(request, template_path, context)
def logout(request):
    auth.logout(request)
    return redirect('Home')
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpass']
        if password == cpass:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'Username already exists')
                return HttpResponseRedirect(reverse('register'))
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.set_password(password)
                user.save()
                return redirect("login_user")
        else:
            messages.add_message(request, messages.ERROR, 'password not matching')
            return HttpResponseRedirect(reverse('register'))
    else:
        return render(request,"register.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index/')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
            return HttpResponseRedirect(reverse('login_user'))


    else:
        return render(request, "login.html")
