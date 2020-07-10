from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def home(request):
	context = {}
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		try:
			User.objects.get(pk = user_id).delete()
			context['msg'] = 'Sucessfully deleted.'
		except:
			context['err'] = 'User not found!'

	items = User.objects.all()
	if not items:
		return HttpResponseRedirect('/')
	context['items'] = items
	return render(request, 'home.html', context)


def login_view(request):
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
                return render(request, 'login.html', {'err':msg, 'login':logged, 'username':username})
        else:
            if User.objects.filter(username = username):
                msg = 'Invalid Password!'
                return render(request, 'login.html', {'err':msg, 'login':logged, 'username':username})
            return HttpResponseRedirect('/signup')

    else:
        return render(request, 'login.html', {})

def signup(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password!=confirm_password:
            context['err'] = 'Passwords Mismatched!'
        try:
            user = User.objects.get(username=username)
            context['err'] = 'User already exists with this username!'
        except:
            pass

        if not context.get('err'):
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.save()
            login(request, user)
            context['msg'] = 'User Created.'
            return HttpResponseRedirect('/')

    return render(request, 'signup.html', context)