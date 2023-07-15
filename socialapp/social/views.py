from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import SignUpForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .models import Users,ChatRoom,Chats
from django.contrib.auth.decorators import login_required
import re
# Create your views here.

@login_required
def index(request):
    users = Users.objects.exclude(pk=request.user.pk).all()
    return render(request,'social/index.html',{'users':users})

class LoginUser(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request,'social/login.html')

    def post(self,request):
        email = request.POST.get('email')
        password =  request.POST.get('password')
        if (not email) or (not password):
            return render(request,'social/login.html',{'error':'Both the fields are required'})
        if email:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email):
                pass
            else:
                return render(request, 'social/login.html', {'error': 'Invalid email address'})
        user = authenticate(username=email.strip(), password=password)
        if user is None:
            # messages.warning(request,'Your email or password is incorrect.')
            return render(request, 'social/login.html', {'error': 'Your Email or Password is incorrect'})
        if not user.is_active:
            return render(request, 'social/login.html', {'error': 'Your account has disabled'})
        messages.success(request,'you are successfully logged in.')
        login(request, user)
        return redirect("/")

    
class RegisterUser(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("/")
        form = SignUpForm()
        return render(request,'social/register.html',{'form': form})

    def post(self,request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'You are successfully Registered.')
            return redirect('/login/')
        return render(request,'social/register.html',{'form': form})


@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login/')

@login_required
def chatting(request,pk,name):
    receiver = get_object_or_404(Users,pk=pk)
    combine=f'{pk}_{request.user.pk}'
    roomName= 'chat__myroom_' + ''.join(sorted(combine))
    users = Users.objects.exclude(pk__in=[request.user.pk]).all()
    context = {'users': users, 'friend': receiver}
    try:
        chatroom = ChatRoom.objects.get(name=roomName)
        chats = Chats.objects.filter(room=chatroom)
        context['chats'] = chats
    except:
        pass

    return render(request,'social/index.html',context)