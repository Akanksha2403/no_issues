from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.utils import timezone
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required

from django.urls import reverse

def escalate_complains(func):
    current_date = timezone.now().date()

    # Get all active complaints that are due for escalation and have a non-null parent designation
    complaints = Complain.objects.filter(
        completed=False,
        response_date__lt=current_date,
        registered_to__parent__isnull=False
    )

    for complaint in complaints:
        # Traverse the hierarchy by following the parent relationships
        parent_designation = complaint.registered_to.parent

        # Keep going up the tree until we find a parent with a designation holder
        while parent_designation is not None and parent_designation.designation_holder is None:
            parent_designation = parent_designation.parent

        # If we found a parent with a designation holder, update the registered_to field
        if parent_designation is not None:
            complaint.registered_to = parent_designation
            complaint.description += f"\n--escalated due to timeout by the {parent_designation.name} at {timezone.now()}"
            complaint.save()
    
    


def check_designation(profile):
    return profile.designation_holder.exists()


def index(request):
    if (request.user.is_authenticated):
        profile = Profile.objects.get(user=request.user)
        answered_complains = Complain.objects.filter(registered_by=profile, completed=True)
        unanswered_complains = Complain.objects.filter(registered_by=profile, completed=False)
        return render(request, 'complainapp/index.html', {'answered_complains': answered_complains, 'unanswered_complains': unanswered_complains})
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
    if (request.method == "POST"):
        complain_id = request.POST.get('complain_id')
        complain = Complain.objects.get(id=complain_id)
        response = request.POST.get('response')
        complain.description = complain.description + f"\nresponse by {complain.registered_to.name}: {response}"
        complain.response_date = now()
        complain.completed = True
        complain.save()
        messages.success(request, "Complain Responded Successfully")
        return redirect('respondComplain')

    if not check_designation(Profile.objects.get(user=request.user)):
        messages.error(request, "You do not hold any designation")
        return redirect('/')
    myprofile = Profile.objects.get(user=request.user)
    designation_set = myprofile.designation_holder.all()
    complains_list = dict()
    for designation in designation_set:
        complains_list[designation] = Complain.objects.filter(
            registered_to=designation, completed=False)
    return render(request, "complainapp/respondcomplain.html", {'complains_list': complains_list, 'designation_holder': True})

def allcomplain(request):
    allcomplain = Complain.objects.all()
   
    return render(request,'complainapp/allcomplains.html',{'allcomplain':allcomplain})

def postlike(request):
    user = request.user
    if(request.method == 'POST'):
        post_id = request.POST.get('cid')
        post_obj = Complain.objects.get(id=post_id)

        if(user in post_obj.likes.all()):
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)
        
        like, created = Like.objects.get_or_create(user=user, post_id = post_id)

        if not created:
            if(like.value == 'like'):
                like.value = 'unlike'
            else:
                like.value = 'like'
        like.save()

    return redirect('allcomplain')


@login_required(login_url='/')
def createComplain(request):
    myprofile = Profile.objects.get(user=request.user)
    all_designations = Designation.objects.all()
    if request.method == 'POST':
        form = ComplainForm(request.POST)
        if form.is_valid():
            complain = form.save(commit=False)
            # complain.registered_to = 
            complain.registered_by = Profile.objects.get(user=request.user)
            complain.registered_date = now()
            complain.completed = False
            complain.save()
            messages.success(request, "Complain Registered Successfully")
        else:
            messages.error(
                request, "Some Error Occured, Please try again or contact us")
        return redirect('createComplain')

    else:
        complainform = ComplainForm()
        return render(request, "complainapp/createcomplain.html", {'complainform': complainform, 'all_designations': all_designations})
