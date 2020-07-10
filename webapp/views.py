from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@login_required()
def logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def home(request):
    context = {}
    # items = models.Item.objects.all()
    # context['items'] = items
    return render(request, 'home.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logged = False
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                logged = True
                return HttpResponseRedirect('/')
            else:
                msg = 'Your account has been disabled!'
                return render(request, 'login.html', {'msg':msg, 'login':logged, 'username':username})
        else:
            msg = "Invalid login details provided!"
            return render(request, 'login.html', {'msg':msg, 'login':logged, 'username':username})

    else:
        return render(request, 'login.html', {})


