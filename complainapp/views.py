from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required


today_date = None

def check_designation(profile): 
    return profile.designation_holder.all().count() != 0


def index(request):
    if (request.user.is_authenticated):
        return render(request, "complainapp/index.html", {'designation_holder': True})
    else:
        signupform = SignupForm()
        loginform = LoginForm()
        return render(request, "complainapp/authentication.html", {'signupform': signupform, 'loginform': loginform})


def handleLogin(request):
    if (request.method == "POST"):
        loginform = LoginForm(request.POST)
        if (loginform.is_valid()):
            email = loginform.cleaned_data['email']
            if (email.endswith('@iiitl.ac.in') == False):
                messages.error(request, "Please use your IIITL email")
                return redirect('/')
            password = loginform.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if (user is not None):
                login(request, user)
                messages.success(
                    request, f"Welcome {user.first_name}, you have logged in successfully.")
                return redirect('/')
            else:
                messages.error(
                    request, "Invalid Credentials, Please try again")
                return redirect('/')
    messages.error(
        request, "Some Error Occured, Please try again or contact us")
    return redirect('/')


def handleSignup(request):
    if (request.method == "POST"):
        signupform = SignupForm(request.POST)
        if (signupform.is_valid()):
            first_name = signupform.cleaned_data['first_name']
            last_name = signupform.cleaned_data['last_name']
            email = signupform.cleaned_data['email']
            if (email.endswith('@iiitl.ac.in') == False):
                messages.error(
                    request, "Please register with your IIITL email")
                return redirect('index')
            pass1 = signupform.cleaned_data['pass1']
            pass2 = signupform.cleaned_data['pass2']
            if (pass1 != pass2):
                messages.error(request, "Passwords do not match")
                return redirect('index')
            # check user already exists
            if (User.objects.filter(username=email).exists()):
                messages.error(request, "User already exists")
                return redirect('index')
            myuser = User.objects.create_user(email, email, pass1)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.save()
            myprofile = Profile(user=myuser, data={})
            myprofile.save()
            messages.success(
                request, "Your account has been successfully created")
            return redirect('index')
    messages.error(
        request, "Some Error Occured, Please try again or contact us")
    return redirect('index')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')

@login_required(login_url='/')
def respondComplain(request):
    if not check_designation(Profile.objects.get(user=request.user)): 
        messages.error(request, "You do not hold any designation")
        return redirect('/')
    myprofile = Profile.objects.get(user=request.user)
    designation_set = myprofile.designation_holder.all()
    complains_list = dict()
    for designation in designation_set:
        complains_list[designation] = Complain.objects.filter(registered_to=designation)
    return render(request, "complainapp/respondcomplain.html", {'complains_list': complains_list, 'designation_holder': True})

@login_required(login_url='/')
def createComplain(request):
    myprofile = Profile.objects.get(user=request.user)
    all_designations = Designation.objects.all()
    if request.method == 'POST':
        form = ComplainForm(request.POST)
        try: 
            if form.is_valid():
                complain = form.save(commit=False)
                complain.registered_by = request.user.profile
                complain.registered_date = now()
                complain.completed = False
                complain.save()
            messages.success(request, "Complain Registered Successfully")
            return redirect('createcomplain')
        except Exception as e:
            messages.error(request, e)
            return redirect('createcomplain')
    else:
        complainform = ComplainForm()
    return render(request, "complainapp/createcomplain.html", {'complainform': complainform, 'all_designations': all_designations})
